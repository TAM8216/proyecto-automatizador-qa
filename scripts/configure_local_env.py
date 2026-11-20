from __future__ import annotations

import secrets
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SUT_ENV = ROOT.parent / "dashboard-legal" / "Backend" / ".env"


def read_env(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    for raw_line in path.read_text(encoding="utf-8-sig").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip().strip('"').strip("'")
    return values


def main() -> None:
    if not SUT_ENV.exists():
        raise SystemExit(f"No existe la configuración local del SUT: {SUT_ENV}")
    source = read_env(SUT_ENV)
    required = ("DB_USER", "DB_PASSWORD", "DB_HOST", "DB_PORT")
    missing = [name for name in required if not source.get(name)]
    if missing:
        raise SystemExit(f"Faltan variables PostgreSQL en Backend/.env: {missing}")

    target = ROOT / ".env"
    existing = read_env(target) if target.exists() else {}
    content = (ROOT / ".env.example").read_text(encoding="utf-8")
    replacements = {
        "QA_DB_HOST=127.0.0.1": f"QA_DB_HOST={source['DB_HOST']}",
        "QA_DB_PORT=5432": f"QA_DB_PORT={source['DB_PORT']}",
        "QA_DB_USER=postgres": f"QA_DB_USER={source['DB_USER']}",
        "QA_DB_PASSWORD=CAMBIAR_LOCALMENTE": f"QA_DB_PASSWORD={source['DB_PASSWORD']}",
    }
    for old, new in replacements.items():
        content = content.replace(old, new, 1)
    for variable in (
        "QA_SUPERADMIN_PASSWORD",
        "QA_ADMIN_PASSWORD",
        "QA_ABOGADO_PASSWORD",
    ):
        secret = existing.get(variable) or secrets.token_urlsafe(18)
        content = content.replace(
            f"{variable}=CAMBIAR_LOCALMENTE",
            f"{variable}={secret}",
        )
    target.write_text(content, encoding="utf-8")
    print(".env local creado; los secretos no se imprimieron.")


if __name__ == "__main__":
    main()

