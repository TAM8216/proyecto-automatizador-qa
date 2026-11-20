from __future__ import annotations

import httpx
import pytest

from backend.api import service
from backend.api.main import app


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.fixture
async def client():
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as value:
        yield value


@pytest.mark.anyio
async def test_catalogo_expone_suites_y_casos_reales(client) -> None:
    response = await client.get("/suites")
    assert response.status_code == 200
    payload = response.json()
    assert any(flow["id"] == "acceso" for flow in payload["flows"])
    assert "smtp_configured" in payload["delivery"]
    assert "smtp_ready" in payload["delivery"]
    assert any(suite["id"] == "regression" for suite in payload["suites"])
    assert next(suite for suite in payload["suites"] if suite["id"] == "smoke")["flow"] == "acceso"
    assert any(
        case["id"] == "TC-LOG-001"
        for suite in payload["suites"]
        for case in suite["cases"]
    )
    load_suite = next(suite for suite in payload["suites"] if suite["id"] == "carga_local")
    assert load_suite["type"] == "no_funcional"
    assert load_suite["cases"][0]["id"] == "TC-PERF-001"


@pytest.mark.anyio
async def test_post_run_valida_email(client) -> None:
    response = await client.post(
        "/runs",
        json={"email": "correo-invalido", "suite": "smoke", "type": "funcional"},
    )
    assert response.status_code == 422


@pytest.mark.anyio
async def test_post_run_persiste_pendiente_y_devuelve_run_id(client, monkeypatch, tmp_path) -> None:
    monkeypatch.setattr(service, "RUNS_ROOT", tmp_path)
    monkeypatch.setattr(service, "enqueue_run", lambda *args, **kwargs: None)
    response = await client.post(
        "/runs",
        json={"email": "qa@example.com", "suite": "smoke", "type": "funcional"},
    )
    assert response.status_code == 202
    accepted = response.json()
    assert accepted["status"] == "PENDIENTE"
    status_response = await client.get(f"/runs/{accepted['run_id']}")
    assert status_response.status_code == 200
    result = status_response.json()
    assert result["requested_email"] == "qa@example.com"
    assert result["selection"]["suites"] == ["smoke"]
    assert all(case["status"] == "NOT RUN" for case in result["cases"])


@pytest.mark.anyio
async def test_get_run_desconocido_devuelve_404(client, monkeypatch, tmp_path) -> None:
    monkeypatch.setattr(service, "RUNS_ROOT", tmp_path)
    response = await client.get("/runs/00000000-0000-0000-0000-000000000000")
    assert response.status_code == 404


@pytest.mark.anyio
async def test_descarga_reporte_generado(client, monkeypatch, tmp_path) -> None:
    monkeypatch.setattr(service, "RUNS_ROOT", tmp_path)
    report_dir = tmp_path / "run-download"
    report_dir.mkdir()
    expected = b"PK-docx-de-prueba"
    (report_dir / "informe_detallado.docx").write_bytes(expected)
    response = await client.get("/runs/run-download/reports/docx")
    assert response.status_code == 200
    assert response.content == expected
    assert "informe_detallado.docx" in response.headers["content-disposition"]


@pytest.mark.anyio
async def test_post_run_acepta_perfil_no_funcional(client, monkeypatch, tmp_path) -> None:
    monkeypatch.setattr(service, "RUNS_ROOT", tmp_path)
    monkeypatch.setattr(service, "enqueue_run", lambda *args, **kwargs: None)
    response = await client.post(
        "/runs",
        json={
            "email": "qa@example.com",
            "type": "no_funcional",
            "suite": "carga_local",
            "users": 5,
            "spawn_rate": 1,
            "duration_seconds": 30,
        },
    )
    assert response.status_code == 202
    result = service.read_result(response.json()["run_id"])
    assert result["selection"]["load"] == {
        "users": 5,
        "spawn_rate": 1.0,
        "duration_seconds": 30,
    }
    assert result["cases"][0]["id"] == "TC-PERF-001"

