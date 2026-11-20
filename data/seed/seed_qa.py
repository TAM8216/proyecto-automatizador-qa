from __future__ import annotations

import sys
from datetime import date

import bcrypt
import psycopg

from backend.config import SAFE_QA_DATABASE, get_settings


def require_secret(value: str, name: str) -> str:
    if not value or value == "CAMBIAR_LOCALMENTE":
        raise RuntimeError(f"Configura {name} en .env antes de ejecutar el seed.")
    return value


def hash_password(value: str) -> str:
    return bcrypt.hashpw(value.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def upsert_user(cursor, *, email: str, password: str, role: str, suffix: str) -> int:
    existing = cursor.execute("SELECT id FROM usuarios WHERE email=%s", (email,)).fetchone()
    values = (
        "Usuario",
        f"QA-{suffix}",
        "Ficticio",
        f"QA{suffix}001",
        70000000,
        email,
        hash_password(password),
        role,
        "activo",
        date.today(),
    )
    if existing:
        cursor.execute(
            """UPDATE usuarios
               SET nombre=%s, apellido_paterno=%s, apellido_materno=%s, ci=%s,
                   contacto=%s, password=%s, rol=%s, estado=%s, creado_en=%s
               WHERE email=%s""",
            values[:5] + values[6:] + (email,),
        )
        return existing[0]
    return cursor.execute(
        """INSERT INTO usuarios
           (nombre, apellido_paterno, apellido_materno, ci, contacto, email,
            password, rol, estado, creado_en)
           VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id""",
        values,
    ).fetchone()[0]


def seed() -> None:
    settings = get_settings()
    credentials = [
        (settings.qa_superadmin_email, require_secret(settings.qa_superadmin_password, "QA_SUPERADMIN_PASSWORD"), "superadmin", "SA"),
        (settings.qa_admin_email, require_secret(settings.qa_admin_password, "QA_ADMIN_PASSWORD"), "admin", "AD"),
        (settings.qa_abogado_email, require_secret(settings.qa_abogado_password, "QA_ABOGADO_PASSWORD"), "abogado", "AB"),
    ]

    with psycopg.connect(**settings.db_kwargs) as connection:
        current = connection.execute("SELECT current_database()").fetchone()[0]
        if current != SAFE_QA_DATABASE:
            raise RuntimeError("Seed bloqueado: la conexión no apunta a la base QA autorizada.")
        required = {"usuarios", "clientes", "casos"}
        existing = {
            row[0]
            for row in connection.execute(
                "SELECT table_name FROM information_schema.tables WHERE table_schema='public'"
            )
        }
        missing = required - existing
        if missing:
            raise RuntimeError(f"Falta el esquema IPAS en la base QA: {sorted(missing)}")

        with connection.cursor() as cursor:
            ids = {
                role: upsert_user(cursor, email=email, password=password, role=role, suffix=suffix)
                for email, password, role, suffix in credentials
            }
            client = cursor.execute("SELECT id FROM clientes WHERE ci='QA-CI-0001'").fetchone()
            if client:
                client_id = client[0]
            else:
                client_id = cursor.execute(
                    """INSERT INTO clientes
                       (nombre, apellido_paterno, apellido_materno, ci, contacto, tipo_cliente)
                       VALUES ('Cliente','Ficticio','QA','QA-CI-0001','70000001','persona')
                       RETURNING id"""
                ).fetchone()[0]
            if not cursor.execute("SELECT 1 FROM casos WHERE nurej_cud='QA-EXP-0001'").fetchone():
                cursor.execute(
                    """INSERT INTO casos
                       (nurej_cud, delito, tipo_caso, asunto, fecha_ingreso, fecha_inicio,
                        materia, creado_por, clientes_id, estado, responsable_id, seguimiento)
                       VALUES ('QA-EXP-0001','Caso ficticio sin delito real','CIVIL',
                        'Expediente sintético exclusivo para automatización',CURRENT_DATE,CURRENT_DATE,
                        'Derecho Civil',%s,%s,'tramite',%s,'recepcion')""",
                    (ids["admin"], client_id, ids["abogado"]),
                )
    print("Seed QA completado: 3 usuarios, 1 cliente y 1 expediente ficticio.")


if __name__ == "__main__":
    try:
        seed()
    except Exception as exc:
        print(f"ERROR SEED QA: {exc}", file=sys.stderr)
        raise SystemExit(2)

