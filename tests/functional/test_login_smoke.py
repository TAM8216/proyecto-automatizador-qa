import pytest

from backend.config import get_settings
from pages.login_page import LoginPage


@pytest.mark.smoke
@pytest.mark.functional
@pytest.mark.login
@pytest.mark.case_id("TC-LOG-001")
def test_login_abogado_valido(driver, evidence_dir):
    """TC-LOG-001: un abogado QA válido accede a su dashboard."""
    settings = get_settings()
    if not settings.qa_abogado_password:
        pytest.fail("QA_ABOGADO_PASSWORD no está configurada en .env")

    page = LoginPage(
        driver,
        str(settings.sut_frontend_url),
        settings.qa_wait_seconds,
    )
    page.open()
    page.save_step(evidence_dir, "TC-LOG-001", 1)
    page.open_login()
    page.save_step(evidence_dir, "TC-LOG-001", 2)
    page.login(settings.qa_abogado_email, settings.qa_abogado_password)
    page.wait_for_dashboard("abogado")
    page.save_step(evidence_dir, "TC-LOG-001", 3)

