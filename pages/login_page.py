from __future__ import annotations

from pathlib import Path

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait


class LoginPage:
    ACCESS_BUTTON = (By.XPATH, "//button[normalize-space()='Acceso equipo']")
    EMAIL = (By.XPATH, "//label[normalize-space()='Correo institucional']/following::input[1]")
    PASSWORD = (By.XPATH, "//label[normalize-space()='Contraseña']/following::input[1]")
    SUBMIT = (By.XPATH, "//button[normalize-space()='Ingresar']")
    DASHBOARD_HEADING = (By.XPATH, "//*[normalize-space()='Mi panel de trabajo']")

    def __init__(self, driver: WebDriver, base_url: str, wait_seconds: int = 15):
        self.driver = driver
        self.base_url = base_url
        self.wait = WebDriverWait(driver, wait_seconds)

    def save_step(self, evidence_dir: Path, case_id: str, number: int) -> Path:
        evidence_dir.mkdir(parents=True, exist_ok=True)
        target = evidence_dir / f"{case_id}_{number}.png"
        self.driver.save_screenshot(str(target))
        return target

    def open(self) -> None:
        self.driver.get(self.base_url)
        self.wait.until(ec.element_to_be_clickable(self.ACCESS_BUTTON))

    def open_login(self) -> None:
        self.wait.until(ec.element_to_be_clickable(self.ACCESS_BUTTON)).click()
        self.wait.until(ec.visibility_of_element_located(self.EMAIL))

    def login(self, email: str, password: str) -> None:
        self.driver.find_element(*self.EMAIL).send_keys(email)
        self.driver.find_element(*self.PASSWORD).send_keys(password)
        self.wait.until(ec.element_to_be_clickable(self.SUBMIT)).click()

    def wait_for_dashboard(self, role: str) -> None:
        expected_fragment = f"/{role}/dashboard"
        self.wait.until(lambda driver: expected_fragment in driver.current_url)
        self.wait.until(ec.visibility_of_element_located(self.DASHBOARD_HEADING))

