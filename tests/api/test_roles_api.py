import pytest


@pytest.mark.api
@pytest.mark.roles
@pytest.mark.controlled_fail
@pytest.mark.case_id("TC-ROL-001")
def test_abogado_no_puede_listar_usuarios(api_client, auth_headers):
    """FAIL controlado: la API debería aplicar RBAC, no solo autenticación."""
    response = api_client.get("/usuarios", headers=auth_headers("abogado"))
    assert response.status_code == 403, (
        "BUG-01-F: un abogado autenticado pudo listar usuarios; "
        f"respuesta HTTP observada={response.status_code}"
    )

