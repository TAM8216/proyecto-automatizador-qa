from __future__ import annotations

import json

import pytest

from backend.ai import service
from backend.ai.provider import AIResponse


class FakeProvider:
    def __init__(self, *payloads: dict):
        self.payloads = list(payloads)

    def complete_json(self, system: str, prompt: str) -> AIResponse:
        assert "PASS/FAIL" in system
        return AIResponse(self.payloads.pop(0), {"provider": "fake", "model": "test"})


@pytest.fixture
def isolated_ai(monkeypatch, tmp_path):
    ai_root = tmp_path / "ia"
    registry = tmp_path / "dom_selectors.json"
    registry.write_text(json.dumps({
        "locators": {
            "login.access_button": {"by": "xpath", "value": "//button[normalize-space()='Acceso equipo']"},
            "login.email": {"by": "xpath", "value": "//input[@name='email']"},
        }
    }), encoding="utf-8")
    monkeypatch.setattr(service, "AI_ROOT", ai_root)
    monkeypatch.setattr(service, "SELECTORS_PATH", registry)
    return ai_root


def test_detecta_ambiguedades_y_persiste_entrada(isolated_ai):
    provider = FakeProvider({
        "summary": "Falta definir el rol.",
        "ambiguities": ["Rol no especificado"],
        "missing_data": ["Credencial QA"],
        "questions": ["¿Qué rol ejecuta el flujo?"],
        "ready_for_generation": True,
    })
    result = service.analyze("Como usuario quiero consultar un expediente jurídico.", "requisito", provider)
    assert result["status"] == "REQUIERE_ACLARACIONES"
    assert result["ready_for_generation"] is False
    record = service.get_record(result["analysis_id"])
    assert record["input"]["requirement"].startswith("Como usuario")


def test_no_genera_sin_aclaraciones(isolated_ai):
    analysis = service.analyze(
        "Como usuario quiero consultar un expediente jurídico.", "requisito",
        FakeProvider({"summary": "Incompleto", "ambiguities": ["Rol"], "missing_data": [], "questions": ["¿Rol?"], "ready_for_generation": False}),
    )
    with pytest.raises(ValueError, match="Responde"):
        service.generate(analysis["analysis_id"], {}, FakeProvider({}))


def test_selector_inventado_bloquea_codigo(isolated_ai):
    analysis = service.analyze(
        "Como abogado quiero abrir un expediente desde la lista de casos.", "requisito",
        FakeProvider({"summary": "Completo", "ambiguities": [], "missing_data": [], "questions": [], "ready_for_generation": True}),
    )
    draft = service.generate(analysis["analysis_id"], {}, FakeProvider({
        "feature": "Consulta de expediente", "scenarios": ["Escenario: abrir caso"],
        "proposed_steps": ["abrir"], "selectors": {"inventado": "#magic"},
        "unverified_selectors": [], "questions": [],
        "pom_code": "CASE = (By.CSS_SELECTOR, '#magic')", "pytest_code": "def test_case(): pass",
    }))
    assert draft["status"] == "REQUIERE_CONFIRMACION_SELECTOR"
    assert "#magic" in draft["unverified_selectors"]
    assert draft["pom_code"] == ""
    with pytest.raises(ValueError, match="selectores"):
        service.review(analysis["analysis_id"], True, "QA", [])


def test_aprobacion_humana_no_ejecuta(isolated_ai):
    analysis = service.analyze(
        "Como abogado quiero abrir el acceso de equipo con credenciales QA.", "requisito",
        FakeProvider({"summary": "Completo", "ambiguities": [], "missing_data": [], "questions": [], "ready_for_generation": True}),
    )
    draft = service.generate(analysis["analysis_id"], {}, FakeProvider({
        "feature": "Acceso", "scenarios": ["Escenario: ingresar"], "proposed_steps": ["abrir acceso"],
        "selectors": {"acceso": "//button[normalize-space()='Acceso equipo']"},
        "unverified_selectors": [], "questions": [], "pom_code": "class LoginPage:\n    pass", "pytest_code": "def test_login():\n    pass",
    }))
    assert draft["gherkin"].startswith("Característica: Acceso")
    assert "Escenario: ingresar" in draft["gherkin"]
    assert "  abrir acceso" in draft["gherkin"]
    review = service.review(analysis["analysis_id"], True, "QA senior", ["Agregar prioridad"])
    assert review["status"] == "APROBADO_PARA_IMPLEMENTACION"
    assert review["execution_started"] is False


def test_codigo_invalido_o_import_peligroso_no_puede_aprobarse(isolated_ai):
    analysis = service.analyze(
        "Como abogado quiero consultar un expediente usando únicamente datos ficticios.", "requisito",
        FakeProvider({"summary": "Completo", "ambiguities": [], "missing_data": [], "questions": [], "ready_for_generation": True}),
    )
    draft = service.generate(analysis["analysis_id"], {}, FakeProvider({
        "feature": "Consulta", "scenarios": ["Escenario: consultar"], "proposed_steps": ["consultar"],
        "selectors": {}, "unverified_selectors": [], "questions": [],
        "pom_code": "class CasesPage:\n    pass", "pytest_code": "import subprocess\ndef test_case(:\n    pass",
    }))
    assert draft["status"] == "REQUIERE_CORRECCION_CODIGO"
    assert any("Python inválido" in issue for issue in draft["validation_issues"])
    assert draft["pytest_code"] == ""
    with pytest.raises(ValueError, match="validar"):
        service.review(analysis["analysis_id"], True, "QA", [])


def test_acepta_prefijo_xpath_y_limpia_bloques_python(isolated_ai):
    analysis = service.analyze(
        "Como abogado quiero acceder usando el botón de acceso verificado.", "requisito",
        FakeProvider({"summary": "Completo", "ambiguities": [], "missing_data": [], "questions": [], "ready_for_generation": True}),
    )
    draft = service.generate(analysis["analysis_id"], {}, FakeProvider({
        "feature": "Acceso de equipo", "scenarios": ["Ingreso válido"],
        "proposed_steps": ["Dado que IPAS está disponible", "Cuando pulso Acceso equipo", "Entonces veo el formulario"],
        "selectors": {"acceso": "xpath://button[normalize-space()='Acceso equipo']"},
        "unverified_selectors": [], "questions": [],
        "pom_code": "```python\nclass LoginPage:\n    pass\n```",
        "pytest_code": "```python\ndef test_login():\n    pass\n```",
    }))
    assert draft["status"] == "BORRADOR_PENDIENTE_APROBACION"
    assert draft["unverified_selectors"] == []
    assert draft["pom_code"].startswith("class LoginPage")
    assert "Escenario: Ingreso válido" in draft["gherkin"]


def test_resumen_conserva_estado_real(isolated_ai, tmp_path):
    run_dir = tmp_path / "run"
    run_dir.mkdir()
    (run_dir / "result.json").write_text(json.dumps({
        "status": "FINALIZADA", "summary": {"pass": 1, "fail": 1},
        "tests": [{"id": "TC-1", "status": "FAIL", "error": "HTTP 500"}],
    }), encoding="utf-8")
    result = service.summarize_failures("run-1", run_dir, FakeProvider({
        "executive_summary": "Un fallo observado.", "failure_explanations": [], "recommended_next_actions": []
    }))
    assert result["execution_status_immutable"] == "FINALIZADA"
    assert result["test_summary_immutable"] == {"pass": 1, "fail": 1}
