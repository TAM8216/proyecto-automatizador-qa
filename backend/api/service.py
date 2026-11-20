from __future__ import annotations

import json
import os
import threading
import traceback
import uuid
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from pathlib import Path
from typing import Any

from backend.config import ROOT
from backend.mailer.service import send_reports
from backend.reports.generator import build_docx, build_html, load_report_data
from backend.runner.catalog import Catalog, TestCase
from backend.runner.load import execute_load
from backend.runner.run import execute


RUNS_ROOT = ROOT / "reports"
MAX_WORKERS = max(1, int(os.getenv("QA_API_RUN_WORKERS", "1")))
RUN_EXECUTOR = ThreadPoolExecutor(max_workers=MAX_WORKERS, thread_name_prefix="ipas-qa-run")
_write_lock = threading.Lock()


def iso_now() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def result_path(run_id: str) -> Path:
    return RUNS_ROOT / run_id / "result.json"


def write_result(run_id: str, payload: dict[str, Any]) -> None:
    path = result_path(run_id)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(".json.tmp")
    with _write_lock:
        temporary.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
        temporary.replace(path)


def read_result(run_id: str) -> dict[str, Any] | None:
    path = result_path(run_id)
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None


def create_pending_run(request, selected: list[TestCase]) -> tuple[str, dict[str, Any], dict[str, Any]]:
    run_id = str(uuid.uuid4())
    selection = {
        "suites": [request.suite] if request.suite else [],
        "case_ids": request.case_ids,
        "all": request.all_cases,
        "type": request.type,
        "load": {
            "users": request.users,
            "spawn_rate": request.spawn_rate,
            "duration_seconds": request.duration_seconds,
        } if request.type == "no_funcional" else None,
    }
    payload = {
        "run_id": run_id,
        "status": "PENDIENTE",
        "failure_type": None,
        "created_at": iso_now(),
        "started_at": None,
        "finished_at": None,
        "duration_seconds": 0,
        "requested_email": str(request.email),
        "selection": selection,
        "health": [],
        "summary": {
            "total": len(selected),
            "pass": 0,
            "fail": 0,
            "skipped": 0,
            "not_run": len(selected),
        },
        "cases": [
            {
                "id": case.id,
                "name": case.name,
                "type": case.type,
                "module": case.module,
                "status": "NOT RUN",
                "failure_type": None,
                "observation": "En espera de ejecución",
                "controlled_fail": case.controlled_fail,
                "defect": case.defect,
            }
            for case in selected
        ],
    }
    write_result(run_id, payload)
    return run_id, selection, payload


def _run_in_background(
    run_id: str,
    selected: list[TestCase],
    selection: dict[str, Any],
    email: str,
) -> None:
    current = read_result(run_id) or {}
    current.update({"status": "EN CURSO", "started_at": iso_now()})
    write_result(run_id, current)
    try:
        engines = {case.engine for case in selected}
        if engines == {"locust"}:
            execute_load(
                selected,
                selection,
                run_id=run_id,
                requested_email=email,
                defer_final_status=True,
            )
        elif engines == {"pytest"}:
            execute(
                selected,
                selection,
                run_id=run_id,
                requested_email=email,
                defer_final_status=True,
            )
        else:
            raise ValueError("No se pueden mezclar motores pytest y Locust en la misma corrida.")
        finalize_reports_and_email(run_id, email)
    except Exception as exc:  # frontera de seguridad del worker
        failed = read_result(run_id) or current
        failed.update(
            {
                "status": "FALLIDA",
                "failure_type": "infraestructura",
                "finished_at": iso_now(),
                "error": f"{exc.__class__.__name__}: {exc}",
                "worker_traceback": traceback.format_exc(limit=8),
            }
        )
        for case in failed.get("cases", []):
            if case.get("status") == "NOT RUN":
                case["failure_type"] = "infraestructura"
                case["observation"] = "El worker no pudo completar la ejecución"
        write_result(run_id, failed)


def suite_name(selection: dict[str, Any]) -> str:
    catalog = Catalog()
    suites = selection.get("suites") or []
    if suites:
        return catalog.suites[suites[0]]["name"]
    if selection.get("all"):
        return "Todos los casos"
    return "Casos específicos"


def finalize_reports_and_email(run_id: str, email: str) -> dict[str, Any]:
    payload = read_result(run_id)
    if payload is None:
        raise FileNotFoundError(f"No existe result.json para el run {run_id}")
    path = result_path(run_id)
    output_dir = path.parent
    docx_path = output_dir / "informe_detallado.docx"
    html_path = output_dir / "reporte_autocontenido.html"
    try:
        report_data = load_report_data(path, email)
        build_docx(report_data, docx_path)
        build_html(report_data, html_path)
        payload["reports"] = {
            "status": "GENERADOS",
            "docx": str(docx_path),
            "html": str(html_path),
            "generated_at": iso_now(),
        }
    except Exception as exc:
        payload.update({"status": "FALLIDA", "failure_type": "infraestructura"})
        payload["reports"] = {
            "status": "FALLIDA",
            "error": f"{exc.__class__.__name__}: no fue posible generar ambos reportes.",
        }
        payload["email_delivery"] = {
            "status": "NO ENVIADO",
            "failure_type": "infraestructura",
            "error": "El envío fue bloqueado porque faltan los dos reportes.",
        }
        write_result(run_id, payload)
        return payload

    delivery = send_reports(
        recipient=email,
        suite_name=suite_name(payload["selection"]),
        docx_path=docx_path,
        html_path=html_path,
        run_id=run_id,
    )
    payload["email_delivery"] = delivery.to_dict()
    if delivery.status == "ENVIADO":
        payload["status"] = payload.get("test_status", "FINALIZADA")
        payload["failure_type"] = (
            payload.get("failure_type") if payload["status"] == "FALLIDA" else None
        )
    else:
        payload["status"] = "FALLIDA"
        payload["failure_type"] = "infraestructura"
    write_result(run_id, payload)
    return payload


def enqueue_run(run_id: str, selected: list[TestCase], selection: dict[str, Any], email: str) -> None:
    RUN_EXECUTOR.submit(_run_in_background, run_id, selected, selection, email)


def select_cases(request) -> list[TestCase]:
    return Catalog().select(
        [request.suite] if request.suite else [],
        request.case_ids,
        request.all_cases,
        request.type,
    )

