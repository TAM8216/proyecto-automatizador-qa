from pathlib import Path

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait


class CasesPage:
    CASES_LINK = (By.XPATH, "//a[.//*[normalize-space()='Casos'] or normalize-space()='Casos']")
    HEADING = (By.XPATH, "//*[normalize-space()='Gestión de Casos']")

    def __init__(self, driver: WebDriver, wait_seconds: int = 15):
        self.driver = driver
        self.wait = WebDriverWait(driver, wait_seconds)

    def open_from_sidebar(self) -> None:
        self.wait.until(ec.element_to_be_clickable(self.CASES_LINK)).click()
        self.wait.until(ec.visibility_of_element_located(self.HEADING))

    def wait_for_case(self, nurej: str) -> None:
        locator = (By.XPATH, f"//*[normalize-space()={nurej!r}]")
        self.wait.until(ec.visibility_of_element_located(locator))

    def save_step(self, evidence_dir: Path, case_id: str, number: int) -> None:
        evidence_dir.mkdir(parents=True, exist_ok=True)
        self.driver.save_screenshot(str(evidence_dir / f"{case_id}_{number}.png"))

