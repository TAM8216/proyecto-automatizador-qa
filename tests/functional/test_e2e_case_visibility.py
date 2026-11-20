import pytest

from backend.config import get_settings
from pages.cases_page import CasesPage
from pages.login_page import LoginPage


@pytest.mark.functional
@pytest.mark.e2e
@pytest.mark.case_id("TC-E2E-001")
def test_abogado_visualiza_expediente_qa(driver, evidence_dir):
    settings = get_settings()
    login = LoginPage(driver, str(settings.sut_frontend_url), settings.qa_wait_seconds)
    login.open()
    login.open_login()
    login.login(settings.qa_abogado_email, settings.qa_abogado_password)
    login.wait_for_dashboard("abogado")
    cases = CasesPage(driver, settings.qa_wait_seconds)
    cases.save_step(evidence_dir, "TC-E2E-001", 1)
    cases.open_from_sidebar()
    cases.wait_for_case("QA-EXP-0001")
    cases.save_step(evidence_dir, "TC-E2E-001", 2)

