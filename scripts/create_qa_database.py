from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path

import psycopg
from psycopg import sql

from backend.config import SAFE_QA_DATABASE, get_settings


ROOT = Path(__file__).resolve().parents[1]
SUT_ROOT = ROOT.parent / "dashboard-legal"
SCHEMA_ARCHIVE = SUT_ROOT / "Backend" / "backups" / "backup_2026-06-23T18-22-19-166Z.sql"
MIGRATIONS = (
    SUT_ROOT / "Backend" / "src" / "migrations" / "migracion_vectores.sql",
    SUT_ROOT / "Backend" / "src" / "migrations" / "20261115_agenda_juridica.sql",
    SUT_ROOT / "Backend" / "src" / "migrations" / "20261115_flujo_cliente.sql",
)


def create_database_if_missing() -> bool:
    settings = get_settings()
    admin = settings.db_kwargs | {"dbname": "postgres"}
    with psycopg.connect(**admin, autocommit=True) as connection:
        exists = connection.execute(
            "SELECT 1 FROM pg_database WHERE datname=%s", (SAFE_QA_DATABASE,)
        ).fetchone()
        if exists:
            return False
        connection.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(SAFE_QA_DATABASE)))
        return True


def public_table_count() -> int:
    settings = get_settings()
    with psycopg.connect(**settings.db_kwargs) as connection:
        return connection.execute(
            "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema='public'"
        ).fetchone()[0]


def restore_schema() -> None:
    settings = get_settings()
    pg_restore = shutil.which("pg_restore")
    if not pg_restore:
        candidate = Path(r"C:\Program Files\PostgreSQL\17\bin\pg_restore.exe")
        pg_restore = str(candidate) if candidate.exists() else None
    if not pg_restore:
        raise RuntimeError("No se encontró pg_restore de PostgreSQL 17.")
    if not SCHEMA_ARCHIVE.exists():
        raise RuntimeError(f"No existe el respaldo de esquema: {SCHEMA_ARCHIVE}")

    environment = os.environ.copy()
    environment["PGPASSWORD"] = settings.qa_db_password
    command = [
        pg_restore,
        "--schema-only",
        "--no-owner",
        "--no-privileges",
        "--exit-on-error",
        "--host", settings.qa_db_host,
        "--port", str(settings.qa_db_port),
        "--username", settings.qa_db_user,
        "--dbname", SAFE_QA_DATABASE,
        str(SCHEMA_ARCHIVE),
    ]
    result = subprocess.run(command, env=environment, text=True, capture_output=True)
    if result.returncode:
        raise RuntimeError(f"pg_restore falló sin restaurar datos: {result.stderr.strip()}")


def apply_migrations() -> None:
    settings = get_settings()
    with psycopg.connect(**settings.db_kwargs, autocommit=True) as connection:
        current = connection.execute("SELECT current_database()").fetchone()[0]
        if current != SAFE_QA_DATABASE:
            raise RuntimeError("Migraciones bloqueadas: destino no autorizado.")
        for migration in MIGRATIONS:
            if not migration.exists():
                raise RuntimeError(f"No existe la migración: {migration}")
            connection.execute(migration.read_text(encoding="utf-8-sig"))
            print(f"Migración aplicada: {migration.name}")


def main() -> None:
    created = create_database_if_missing()
    count = public_table_count()
    if count == 0:
        restore_schema()
        print("Esquema IPAS restaurado sin datos.")
    else:
        print(f"Base QA existente; restauración omitida (tablas públicas={count}).")
    apply_migrations()
    print(f"Base segura lista: {SAFE_QA_DATABASE}; creada={created}; tablas={public_table_count()}")


if __name__ == "__main__":
    main()

