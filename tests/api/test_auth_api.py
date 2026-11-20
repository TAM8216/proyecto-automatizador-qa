import pytest


@pytest.mark.api
@pytest.mark.login
@pytest.mark.case_id("TC-LOG-002")
def test_login_rechaza_password_incorrecto(api_client, settings):
    response = api_client.post(
        "/auth/login",
        json={"email": settings.qa_abogado_email, "password": "incorrecta-qa"},
    )
    assert response.status_code == 401
    assert response.json()["message"] == "Password incorrecto"


@pytest.mark.api
@pytest.mark.login
@pytest.mark.case_id("TC-LOG-003")
def test_login_requiere_email(api_client):
    response = api_client.post("/auth/login", json={"email": "", "password": "x"})
    assert response.status_code == 400
    assert "obligatorios" in response.json()["message"]


@pytest.mark.api
@pytest.mark.login
@pytest.mark.case_id("TC-LOG-004")
def test_verify_acepta_token_valido(api_client, auth_headers, settings):
    response = api_client.get("/auth/verify", headers=auth_headers("abogado"))
    assert response.status_code == 200
    assert response.json()["user"]["rol"] == "abogado"
    assert response.json()["user"]["email"] == settings.qa_abogado_email

