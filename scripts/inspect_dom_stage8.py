from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

from dotenv import dotenv_values
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait


LOCATORS = {
    "login.access_button": ("xpath", "//button[normalize-space()='Acceso equipo']"),
    "login.email": ("xpath", "//label[normalize-space()='Correo institucional']/following::input[1]"),
    "login.password": ("xpath", "//label[normalize-space()='Contraseña']/following::input[1]"),
    "login.submit": ("xpath", "//button[normalize-space()='Ingresar']"),
    "dashboard.heading": ("xpath", "//*[normalize-space()='Mi panel de trabajo']"),
    "cases.navigation": ("xpath", "//a[.//*[normalize-space()='Casos'] or normalize-space()='Casos']"),
    "cases.heading": ("xpath", "//*[normalize-space()='Gestión de Casos']"),
}


def main() -> int:
    parser = argparse.ArgumentParser(description="Audita locators de IPAS contra el DOM local real.")
    parser.add_argument("--env-file", type=Path, required=True)
    parser.add_argument("--driver", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--headless", action="store_true")
    args = parser.parse_args()

    environment = dotenv_values(args.env_file)
    base_url = environment.get("SUT_FRONTEND_URL", "http://127.0.0.1:3000")
    email = environment.get("QA_ABOGADO_EMAIL", "")
    password = environment.get("QA_ABOGADO_PASSWORD", "")
    if not email or not password:
        raise SystemExit("Faltan credenciales QA en el archivo de entorno indicado.")

    options = webdriver.EdgeOptions()
    edge_binary = Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe")
    if edge_binary.exists():
        options.binary_location = str(edge_binary)
    if args.headless:
        options.add_argument("--headless=new")
    driver = webdriver.Edge(service=Service(str(args.driver)), options=options)
    driver.set_window_size(1440, 1000)
    wait = WebDriverWait(driver, 20)
    verified: dict[str, dict[str, str]] = {}

    try:
        driver.get(str(base_url))
        for name in ("login.access_button",):
            by, value = LOCATORS[name]
            wait.until(ec.element_to_be_clickable((By.XPATH, value)))
            verified[name] = {"by": by, "value": value}
        driver.find_element(By.XPATH, LOCATORS["login.access_button"][1]).click()

        for name in ("login.email", "login.password", "login.submit"):
            by, value = LOCATORS[name]
            wait.until(ec.visibility_of_element_located((By.XPATH, value)))
            verified[name] = {"by": by, "value": value}

        driver.find_element(By.XPATH, LOCATORS["login.email"][1]).send_keys(email)
        driver.find_element(By.XPATH, LOCATORS["login.password"][1]).send_keys(password)
        driver.find_element(By.XPATH, LOCATORS["login.submit"][1]).click()

        for name in ("dashboard.heading", "cases.navigation"):
            by, value = LOCATORS[name]
            wait.until(ec.visibility_of_element_located((By.XPATH, value)))
            verified[name] = {"by": by, "value": value}

        driver.find_element(By.XPATH, LOCATORS["cases.navigation"][1]).click()
        by, value = LOCATORS["cases.heading"]
        wait.until(ec.visibility_of_element_located((By.XPATH, value)))
        verified["cases.heading"] = {"by": by, "value": value}

        payload = {
            "schema_version": 1,
            "sut": "IPAS / IUS PUNIENDI local QA",
            "verified_at": datetime.now(timezone.utc).isoformat(),
            "verification_method": "Selenium Edge contra DOM renderizado; cada locator fue visible o accionable.",
            "base_url": str(base_url),
            "locators": verified,
        }
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(json.dumps({"verified": len(verified), "output": str(args.output)}, ensure_ascii=False))
        return 0
    finally:
        driver.quit()


if __name__ == "__main__":
    raise SystemExit(main())
