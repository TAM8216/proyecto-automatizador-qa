import pytest

from backend.runner.health import run_checks


@pytest.mark.smoke
@pytest.mark.api
@pytest.mark.case_id("TC-SMK-001")
def test_ipas_local_health():
    checks = run_checks()
    failures = [f"{check.component}: {check.detail}" for check in checks if not check.ok]
    assert not failures, " | ".join(failures)

