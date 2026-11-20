from __future__ import annotations

import json
import sys
from dataclasses import asdict, dataclass

import httpx
import psycopg

from backend.config import SAFE_QA_DATABASE, get_settings


@dataclass
class Check:
    component: str
    ok: bool
    detail: str


def check_http(component: str, url: str, accepted: set[int]) -> Check:
    try:
        response = httpx.get(url, timeout=5, follow_redirects=True)
        ok = response.status_code in accepted
        return Check(component, ok, f"HTTP {response.status_code}")
    except httpx.HTTPError as exc:
        return Check(component, False, f"Sin respuesta: {exc.__class__.__name__}")


def check_database() -> Check:
    settings = get_settings()
    try:
        with psycopg.connect(**settings.db_kwargs, connect_timeout=5) as connection:
            name = connection.execute("SELECT current_database()").fetchone()[0]
            tables = connection.execute(
                "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema='public'"
            ).fetchone()[0]
        if name != SAFE_QA_DATABASE:
            return Check("database", False, "Nombre de base no autorizado")
        return Check("database", True, f"{name}; tablas públicas={tables}")
    except psycopg.Error as exc:
        return Check("database", False, f"No disponible: {exc.__class__.__name__}")


def run_checks() -> list[Check]:
    settings = get_settings()
    return [
        check_http("frontend", str(settings.sut_frontend_url), {200}),
        check_http(
            "api",
            f"{str(settings.sut_api_url).rstrip('/')}/auth/verify",
            {401},
        ),
        check_database(),
    ]


def main() -> int:
    checks = run_checks()
    print(json.dumps([asdict(check) for check in checks], indent=2, ensure_ascii=False))
    return 0 if all(check.ok for check in checks) else 2


if __name__ == "__main__":
    sys.exit(main())

