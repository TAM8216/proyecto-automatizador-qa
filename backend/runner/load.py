from __future__ import annotations

import csv
import json
import subprocess
import sys
import uuid
from datetime import datetime
from pathlib import Path
from time import perf_counter

from backend.config import ROOT, get_settings
from backend.runner.catalog import TestCase
from backend.runner.health import run_checks


def iso_now() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def number(row: dict[str, str], key: str, default: float = 0.0) -> float:
    try:
        return float(row.get(key) or default)
    except ValueError:
        return default


def parse_stats(path: Path) -> tuple[dict, list[dict]]:
    with path.open(encoding="utf-8-sig", newline="") as stream:
        rows = list(csv.DictReader(stream))
    aggregate = next((row for row in rows if row.get("Name") == "Aggregated"), None)
    if aggregate is None:
        raise ValueError("Locust no generó la fila agregada de métricas.")
    requests = int(number(aggregate, "Request Count"))
    failures = int(number(aggregate, "Failure Count"))
    metrics = {
        "requests": requests,
        "failures": failures,
        "error_rate": round(failures / requests if requests else 1.0, 6),
        "throughput_rps": round(number(aggregate, "Requests/s"), 3),
        "average_ms": round(number(aggregate, "Average Response Time"), 3),
        "median_ms": round(number(aggregate, "Median Response Time"), 3),
        "p95_ms": round(number(aggregate, "95%"), 3),
        "min_ms": round(number(aggregate, "Min Response Time"), 3),
        "max_ms": round(number(aggregate, "Max Response Time"), 3),
    }
    endpoints = [
        {
            "method": row.get("Type"),
            "name": row.get("Name"),
            "requests": int(number(row, "Request Count")),
            "failures": int(number(row, "Failure Count")),
            "average_ms": round(number(row, "Average Response Time"), 3),
            "p95_ms": round(number(row, "95%"), 3),
            "rps": round(number(row, "Requests/s"), 3),
        }
        for row in rows
        if row.get("Name") != "Aggregated"
    ]
    return metrics, endpoints


def execute_load(
    selected: list[TestCase],
    selection: dict,
    *,
    run_id: str | None = None,
    requested_email: str = "",
    defer_final_status: bool = False,
) -> tuple[dict, int]:
    settings = get_settings()
    run_id = run_id or str(uuid.uuid4())
    started_at = iso_now()
    clock = perf_counter()
    run_dir = ROOT / "reports" / run_id
    run_dir.mkdir(parents=True, exist_ok=True)
    result_path = run_dir / "result.json"
    checks = run_checks()
    health = [check.__dict__ for check in checks]
    if not all(check.ok for check in checks):
        cases = [{
            "id": case.id,
            "name": case.name,
            "type": case.type,
            "module": case.module,
            "status": "NOT RUN",
            "failure_type": "infraestructura",
            "observation": "Preflight de IPAS falló",
            "controlled_fail": False,
            "defect": None,
        } for case in selected]
        payload = {
            "run_id": run_id,
            "status": "EN CURSO" if defer_final_status else "FALLIDA",
            "test_status": "FALLIDA",
            "failure_type": "infraestructura",
            "started_at": started_at,
            "finished_at": iso_now(),
            "duration_seconds": round(perf_counter() - clock, 3),
            "selection": selection,
            "requested_email": requested_email,
            "health": health,
            "summary": {"total": len(cases), "pass": 0, "fail": 0, "skipped": 0, "not_run": len(cases)},
            "cases": cases,
        }
        result_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
        return payload, 2

    load = selection.get("load") or {}
    users = int(load.get("users") or settings.qa_load_users)
    spawn_rate = float(load.get("spawn_rate") or settings.qa_load_spawn_rate)
    duration = int(load.get("duration_seconds") or settings.qa_load_duration_seconds)
    csv_prefix = run_dir / "locust"
    command = [
        sys.executable, "-m", "locust",
        "-f", str(ROOT / "tests" / "non_functional" / "locustfile.py"),
        "--headless",
        "--host", str(settings.sut_api_url).rstrip("/"),
        "--users", str(users),
        "--spawn-rate", str(spawn_rate),
        "--run-time", f"{duration}s",
        "--stop-timeout", "5",
        "--csv", str(csv_prefix),
        "--only-summary",
    ]
    process = subprocess.run(command, cwd=ROOT, text=True, capture_output=True)
    (run_dir / "locust.log").write_text(process.stdout + process.stderr, encoding="utf-8")
    stats_path = Path(f"{csv_prefix}_stats.csv")
    infrastructure_error = process.returncode not in {0, 1} or not stats_path.exists()
    if infrastructure_error:
        metrics = {}
        endpoints = []
        passed = False
        observation = "Locust no pudo completar la ejecución o no generó métricas."
        failure_type = "infraestructura"
    else:
        metrics, endpoints = parse_stats(stats_path)
        passed = (
            metrics["p95_ms"] < settings.qa_load_p95_limit_ms
            and metrics["error_rate"] < settings.qa_load_error_rate_limit
        )
        observation = (
            f"p95={metrics['p95_ms']} ms; errores={metrics['error_rate'] * 100:.2f}%; "
            f"throughput={metrics['throughput_rps']} req/s"
        )
        failure_type = None if passed else "funcional"

    case_status = "PASS" if passed else "FAIL"
    cases = [{
        "id": case.id,
        "name": case.name,
        "type": case.type,
        "module": case.module,
        "status": case_status,
        "failure_type": failure_type,
        "observation": observation,
        "controlled_fail": False,
        "defect": None,
        "duration_seconds": round(perf_counter() - clock, 3),
    } for case in selected]
    terminal_status = "FINALIZADA" if passed else "FALLIDA"
    payload = {
        "run_id": run_id,
        "status": "EN CURSO" if defer_final_status else terminal_status,
        "test_status": terminal_status,
        "failure_type": failure_type,
        "started_at": started_at,
        "finished_at": iso_now(),
        "duration_seconds": round(perf_counter() - clock, 3),
        "selection": selection,
        "requested_email": requested_email,
        "health": health,
        "summary": {"total": len(cases), "pass": len(cases) if passed else 0, "fail": 0 if passed else len(cases), "skipped": 0, "not_run": 0},
        "performance": {
            "profile": {"users": users, "spawn_rate": spawn_rate, "duration_seconds": duration},
            "criteria": {"p95_limit_ms": settings.qa_load_p95_limit_ms, "error_rate_limit": settings.qa_load_error_rate_limit},
            "aggregate": metrics,
            "endpoints": endpoints,
        },
        "cases": cases,
    }
    result_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    return payload, 0 if passed else 1
