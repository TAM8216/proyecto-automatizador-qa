from uuid import uuid4

import pytest


@pytest.mark.api
@pytest.mark.expedientes
@pytest.mark.case_id("TC-EXP-001")
def test_crear_expediente_valido(api_client, auth_headers):
    nurej = f"QA-AUTO-{uuid4().hex[:10]}"
    response = api_client.post(
        "/casos",
        headers=auth_headers("abogado"),
        json={
            "nurej_cud": nurej,
            "delito": "Caso sintético para prueba positiva",
            "tipo_caso": "CIVIL",
            "asunto": "Creación automatizada en base QA",
            "fecha_ingreso": "2026-11-16",
            "materia": "Derecho Civil",
            "estado": "activo",
        },
    )
    assert response.status_code == 201, response.text
    created = response.json()
    assert created["nurej_cud"] == nurej
    cleanup = api_client.delete(f"/casos/{created['id']}", headers=auth_headers("admin"))
    assert cleanup.status_code == 204


@pytest.mark.api
@pytest.mark.expedientes
@pytest.mark.case_id("TC-EXP-002")
def test_crear_expediente_sin_campo_obligatorio(api_client, auth_headers):
    response = api_client.post(
        "/casos",
        headers=auth_headers("abogado"),
        json={"tipo_caso": "CIVIL", "asunto": "Falta delito"},
    )
    assert response.status_code == 400
    assert "requeridos" in response.json()["message"]


@pytest.mark.api
@pytest.mark.expedientes
@pytest.mark.case_id("TC-EXP-003")
def test_consultar_expediente_inexistente(api_client, auth_headers):
    response = api_client.get("/casos/999999999", headers=auth_headers("abogado"))
    assert response.status_code == 404

