import pytest


@pytest.mark.api
@pytest.mark.public
@pytest.mark.case_id("TC-PUB-001")
def test_seguimiento_publico_valido(api_client):
    response = api_client.get("/seguimiento/publico/QA-EXP-0001", params={"ci": "QA-CI-0001"})
    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    assert body["data"]["nurej_cud"] == "QA-EXP-0001"


@pytest.mark.api
@pytest.mark.public
@pytest.mark.case_id("TC-PUB-002")
def test_seguimiento_publico_ci_incorrecto(api_client):
    response = api_client.get("/seguimiento/publico/QA-EXP-0001", params={"ci": "CI-NO-VALIDO"})
    assert response.status_code == 404
    assert response.json()["success"] is False

