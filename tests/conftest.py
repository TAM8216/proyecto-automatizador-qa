from __future__ import annotations

import uuid
from pathlib import Path

import pytest
import httpx
from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService

from backend.config import ROOT, get_settings


@pytest.fixture(scope="session")
def settings():
    return get_settings()


@pytest.fixture(scope="session")
def api_client(settings):
    with httpx.Client(base_url=str(settings.sut_api_url), timeout=30) as client:
        yield client


@pytest.fixture(scope="session")
def auth_headers(api_client, settings):
    credentials = {
        "superadmin": (settings.qa_superadmin_email, settings.qa_superadmin_password),
        "admin": (settings.qa_admin_email, settings.qa_admin_password),
        "abogado": (settings.qa_abogado_email, settings.qa_abogado_password),
    }
    cache = {}

    def build(role: str) -> dict[str, str]:
        if role not in cache:
            email, password = credentials[role]
            response = api_client.post("/auth/login", json={"email": email, "password": password})
            assert response.status_code == 200, f"No se pudo autenticar fixture {role}: HTTP {response.status_code}"
            cache[role] = response.json()["token"]
        return {"Authorization": f"Bearer {cache[role]}"}

    return build


@pytest.fixture(scope="session")
def qa_case_id(api_client, auth_headers) -> int:
    response = api_client.get("/casos", headers=auth_headers("abogado"))
    assert response.status_code == 200
    case = next((item for item in response.json() if item["nurej_cud"] == "QA-EXP-0001"), None)
    assert case is not None, "El seed QA no contiene QA-EXP-0001"
    return case["id"]


def pytest_addoption(parser):
    parser.addoption("--run-id", action="store", default=None)


@pytest.fixture(scope="session")
def run_id(request) -> str:
    return request.config.getoption("--run-id") or str(uuid.uuid4())


@pytest.fixture
def evidence_dir(run_id: str, request) -> Path:
    case_id = request.node.get_closest_marker("case_id")
    case_name = case_id.args[0] if case_id else request.node.name
    return ROOT / "evidencias" / run_id / case_name


@pytest.fixture
def driver():
    settings = get_settings()
    browser = settings.qa_browser.lower()
    if browser == "edge":
        options = webdriver.EdgeOptions()
        edge_binary = Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe")
        if edge_binary.exists():
            options.binary_location = str(edge_binary)
        if settings.qa_headless:
            options.add_argument("--headless=new")
        driver_binary = ROOT / ".drivers" / "msedgedriver.exe"
        service = EdgeService(executable_path=str(driver_binary)) if driver_binary.exists() else EdgeService()
        instance = webdriver.Edge(service=service, options=options)
    elif browser == "chrome":
        options = webdriver.ChromeOptions()
        if settings.qa_headless:
            options.add_argument("--headless=new")
        instance = webdriver.Chrome(options=options)
    else:
        raise RuntimeError(f"Navegador no soportado: {browser}")
    instance.set_window_size(1440, 1000)
    yield instance
    instance.quit()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed:
        browser = item.funcargs.get("driver")
        directory = item.funcargs.get("evidence_dir")
        if browser and directory:
            directory.mkdir(parents=True, exist_ok=True)
            browser.save_screenshot(str(directory / f"{item.name}_FAIL.png"))

