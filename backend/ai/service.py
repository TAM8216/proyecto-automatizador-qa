from __future__ import annotations

import ast
import json
import re
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from backend.ai.provider import AIProvider, get_ai_provider
from backend.config import ROOT


AI_ROOT = ROOT / "docs" / "ia"
SELECTORS_PATH = ROOT / "config" / "dom_selectors.json"
SYSTEM = (
    "Eres un ingeniero QA senior del dominio jurídico boliviano. Responde exclusivamente JSON válido. "
    "No inventes requisitos, datos, endpoints, estados, credenciales ni selectores. La ejecución real es la "
    "única fuente de PASS/FAIL y tu salida siempre requiere revisión humana."
)


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _directory(identifier: str) -> Path:
    try:
        safe = str(uuid.UUID(identifier))
    except ValueError as exc:
        raise ValueError("Identificador IA inválido.") from exc
    return AI_ROOT / safe


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)


def _read_json(path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise FileNotFoundError("Registro IA no encontrado.")
    return json.loads(path.read_text(encoding="utf-8"))


def _canonical_selector(value: Any) -> str:
    selector = str(value).strip()
    for prefix in ("xpath:", "css:", "css_selector:"):
        if selector.lower().startswith(prefix):
            return selector[len(prefix):].strip()
    return selector


def _clean_python_code(value: Any) -> str:
    code = str(value or "").strip()
    fenced = re.fullmatch(r"```(?:python)?\s*(.*?)\s*```", code, flags=re.DOTALL | re.IGNORECASE)
    return fenced.group(1).strip() if fenced else code


def _normalize_gherkin(feature: Any, scenarios: Any, proposed_steps: Any) -> tuple[str, list[str], list[str], str]:
    feature_text = str(feature or "").strip()
    if not feature_text.lower().startswith(("característica:", "caracteristica:", "feature:")):
        feature_text = f"Característica: {feature_text or 'Escenario jurídico propuesto'}"

    normalized_scenarios: list[str] = []
    for index, scenario in enumerate(scenarios if isinstance(scenarios, list) else []):
        scenario_text = str(scenario).strip()
        if not scenario_text.lower().startswith(("escenario:", "esquema del escenario:", "scenario:")):
            scenario_text = f"Escenario: {scenario_text or f'Escenario propuesto {index + 1}'}"
        normalized_scenarios.append(scenario_text)
    if not normalized_scenarios:
        normalized_scenarios = ["Escenario: Escenario propuesto para revisión"]

    normalized_steps = [str(step).strip() for step in (proposed_steps or []) if str(step).strip()]
    lines = [feature_text, "", normalized_scenarios[0]]
    lines.extend(f"  {step}" for step in normalized_steps)
    for scenario in normalized_scenarios[1:]:
        lines.extend(("", scenario))
    return feature_text, normalized_scenarios, normalized_steps, "\n".join(lines)


def analyze(requirement: str, source_type: str, provider: AIProvider | None = None) -> dict[str, Any]:
    identifier = str(uuid.uuid4())
    directory = _directory(identifier)
    prompt = f"""Analiza el siguiente {source_type}. Detecta ambigüedades y datos faltantes antes de generar pruebas.
Devuelve exactamente: {{"summary": str, "ambiguities": [str], "missing_data": [str],
"questions": [str], "ready_for_generation": bool}}.

ENTRADA DEL USUARIO:
{requirement}
"""
    directory.mkdir(parents=True, exist_ok=False)
    _write_json(directory / "input.json", {
        "analysis_id": identifier, "source_type": source_type, "requirement": requirement, "created_at": _now()
    })
    (directory / "analysis_prompt.txt").write_text(prompt, encoding="utf-8")
    response = (provider or get_ai_provider()).complete_json(SYSTEM, prompt)
    data = response.payload
    analysis = {
        "analysis_id": identifier,
        "summary": str(data.get("summary", "")),
        "ambiguities": [str(item) for item in data.get("ambiguities", [])],
        "missing_data": [str(item) for item in data.get("missing_data", [])],
        "questions": [str(item) for item in data.get("questions", [])],
        "ready_for_generation": bool(data.get("ready_for_generation", False)),
        "status": "LISTO_PARA_GENERAR" if data.get("ready_for_generation") else "REQUIERE_ACLARACIONES",
        "provider": response.metadata,
        "created_at": _now(),
    }
    if analysis["ambiguities"] or analysis["missing_data"] or analysis["questions"]:
        analysis["ready_for_generation"] = False
        analysis["status"] = "REQUIERE_ACLARACIONES"
    _write_json(directory / "analysis.json", analysis)
    return analysis


def _selector_violations(payload: dict[str, Any], allowed: set[str]) -> list[str]:
    proposed = payload.get("selectors", {})
    values = proposed.values() if isinstance(proposed, dict) else []
    violations = [str(value) for value in values if _canonical_selector(value) not in allowed]
    return sorted(set(violations))


def _code_validation_issues(payload: dict[str, Any], allowed: set[str]) -> list[str]:
    issues: list[str] = []
    forbidden_modules = {"os", "subprocess", "socket", "shutil", "requests", "httpx"}
    for field in ("pom_code", "pytest_code"):
        code = _clean_python_code(payload.get(field, ""))
        if not code.strip():
            issues.append(f"{field}: código vacío")
            continue
        try:
            tree = ast.parse(code)
        except SyntaxError as exc:
            issues.append(f"{field}: Python inválido en línea {exc.lineno}")
            continue
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                names = {alias.name.split(".")[0] for alias in node.names}
                if names & forbidden_modules:
                    issues.append(f"{field}: importación no permitida {sorted(names & forbidden_modules)[0]}")
            if isinstance(node, ast.ImportFrom) and (node.module or "").split(".")[0] in forbidden_modules:
                issues.append(f"{field}: importación no permitida {(node.module or '').split('.')[0]}")
            if isinstance(node, ast.Tuple) and len(node.elts) == 2:
                first, second = node.elts
                is_by = isinstance(first, ast.Attribute) and isinstance(first.value, ast.Name) and first.value.id == "By"
                if is_by and isinstance(second, ast.Constant) and isinstance(second.value, str) and second.value not in allowed:
                    issues.append(f"{field}: locator no verificado {second.value}")
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
                if node.func.attr in {"find_element", "find_elements"} and len(node.args) >= 2:
                    candidate = node.args[1]
                    if isinstance(candidate, ast.Constant) and isinstance(candidate.value, str) and candidate.value not in allowed:
                        issues.append(f"{field}: locator no verificado {candidate.value}")
    return sorted(set(issues))


def generate(analysis_id: str, clarifications: dict[str, str], provider: AIProvider | None = None) -> dict[str, Any]:
    directory = _directory(analysis_id)
    analysis = _read_json(directory / "analysis.json")
    source = _read_json(directory / "input.json")
    if not analysis.get("ready_for_generation") and not any(value.strip() for value in clarifications.values()):
        raise ValueError("Responde las preguntas pendientes antes de generar el borrador.")
    registry = _read_json(SELECTORS_PATH)
    prompt = f"""Genera un BORRADOR en español para revisión humana a partir del requisito y aclaraciones.
Usa solamente selectores del REGISTRO DOM. Si falta uno, inclúyelo en unverified_selectors y formula una pregunta;
no generes un locator alternativo. Cada elemento de scenarios debe comenzar con "Escenario:" y proposed_steps
debe usar Dado/Cuando/Entonces/Y. Devuelve código Python plano, sin bloques Markdown. Devuelve exactamente:
{{"feature": str, "scenarios": [str],
"proposed_steps": [str], "selectors": {{str: str}}, "unverified_selectors": [str], "questions": [str],
"pom_code": str, "pytest_code": str}}. Gherkin y nombres del dominio jurídico deben estar en español.

REQUISITO:
{source['requirement']}

ANÁLISIS:
{json.dumps(analysis, ensure_ascii=False)}

ACLARACIONES HUMANAS:
{json.dumps(clarifications, ensure_ascii=False)}

REGISTRO DOM VERIFICADO:
{json.dumps(registry, ensure_ascii=False)}
"""
    (directory / "generation_prompt.txt").write_text(prompt, encoding="utf-8")
    response = (provider or get_ai_provider()).complete_json(SYSTEM, prompt)
    payload = response.payload
    allowed = {item["value"] for item in registry.get("locators", {}).values()}
    violations = _selector_violations(payload, allowed)
    validation_issues = _code_validation_issues(payload, allowed)
    unverified = [str(item) for item in payload.get("unverified_selectors", [])] + violations
    feature, scenarios, proposed_steps, gherkin = _normalize_gherkin(
        payload.get("feature"), payload.get("scenarios"), payload.get("proposed_steps")
    )
    if unverified:
        status = "REQUIERE_CONFIRMACION_SELECTOR"
    elif validation_issues:
        status = "REQUIERE_CORRECCION_CODIGO"
    else:
        status = "BORRADOR_PENDIENTE_APROBACION"
    generation = {
        "analysis_id": analysis_id,
        "status": status,
        "feature": feature,
        "scenarios": scenarios,
        "proposed_steps": proposed_steps,
        "gherkin": gherkin,
        "selectors": payload.get("selectors", {}),
        "unverified_selectors": sorted(set(unverified)),
        "questions": [str(item) for item in payload.get("questions", [])],
        "validation_issues": validation_issues,
        "pom_code": "" if violations or validation_issues else _clean_python_code(payload.get("pom_code", "")),
        "pytest_code": "" if violations or validation_issues else _clean_python_code(payload.get("pytest_code", "")),
        "provider": response.metadata,
        "created_at": _now(),
        "execution_started": False,
    }
    _write_json(directory / "clarifications.json", {"answers": clarifications, "recorded_at": _now()})
    _write_json(directory / "generation.json", generation)
    return generation


def review(analysis_id: str, approved: bool, reviewer: str, corrections: list[str]) -> dict[str, Any]:
    directory = _directory(analysis_id)
    generation = _read_json(directory / "generation.json")
    if approved and generation.get("status") in {"REQUIERE_CONFIRMACION_SELECTOR", "REQUIERE_CORRECCION_CODIGO"}:
        raise ValueError("No se puede aprobar mientras existan selectores o código sin validar.")
    result = {
        "analysis_id": analysis_id,
        "approved": approved,
        "reviewer": reviewer,
        "corrections": corrections,
        "status": "APROBADO_PARA_IMPLEMENTACION" if approved else "CAMBIOS_SOLICITADOS",
        "execution_started": False,
        "recorded_at": _now(),
    }
    _write_json(directory / "human_review.json", result)
    return result


def get_record(analysis_id: str) -> dict[str, Any]:
    directory = _directory(analysis_id)
    result = {"input": _read_json(directory / "input.json"), "analysis": _read_json(directory / "analysis.json")}
    for key, filename in (("generation", "generation.json"), ("review", "human_review.json")):
        if (directory / filename).is_file():
            result[key] = _read_json(directory / filename)
    return result


def summarize_failures(run_id: str, run_directory: Path, provider: AIProvider | None = None) -> dict[str, Any]:
    result = _read_json(run_directory / "result.json")
    executed_cases = result.get("tests") or result.get("cases", [])
    failures = [item for item in executed_cases if item.get("status") == "FAIL"]
    evidence = {
        "run_id": run_id,
        "execution_status": result.get("status"),
        "summary": result.get("summary", {}),
        "failures": failures,
    }
    prompt = f"""Resume fallos reales sin cambiar estados ni inventar causas. Devuelve:
{{"executive_summary": str, "failure_explanations": [{{"case_id": str, "observed": str,
"possible_causes": [str], "evidence": [str]}}], "recommended_next_actions": [str]}}.
EVIDENCIA DE EJECUCIÓN:
{json.dumps(evidence, ensure_ascii=False)}"""
    response = (provider or get_ai_provider()).complete_json(SYSTEM, prompt)
    summary = {
        **response.payload,
        "run_id": run_id,
        "execution_status_immutable": result.get("status"),
        "test_summary_immutable": result.get("summary", {}),
        "provider": response.metadata,
        "created_at": _now(),
    }
    output = AI_ROOT / "run-summaries" / run_id
    output.mkdir(parents=True, exist_ok=True)
    (output / "summary_prompt.txt").write_text(prompt, encoding="utf-8")
    _write_json(output / "summary.json", summary)
    return summary
