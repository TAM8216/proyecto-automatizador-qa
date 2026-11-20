from __future__ import annotations

import argparse
import json
import subprocess
import sys
import uuid
import xml.etree.ElementTree as et
from datetime import datetime
from pathlib import Path
from time import perf_counter

from backend.config import ROOT
from backend.runner.catalog import Catalog, TestCase
from backend.runner.health import run_checks


def iso_now() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def result_stub(case: TestCase, status: str, observation: str = "") -> dict:
    return {
        "id": case.id,
        "name": case.name,
        "type": case.type,
        "module": case.module,
        "status": status,
        "failure_type": None,
        "observation": observation,
        "controlled_fail": case.controlled_fail,
        "defect": case.defect,
    }


def parse_junit(path: Path, selected: list[TestCase]) -> list[dict]:
    root = et.parse(path).getroot()
    junit_cases = list(root.iter("testcase"))
    results: list[dict] = []
    for case in selected:
        test_name = case.nodeid.rsplit("::", 1)[-1]
        node = next((item for item in junit_cases if item.attrib.get("name") == test_name), None)
        if node is None:
            results.append(result_stub(case, "NOT RUN", "pytest no devolvió resultado para el nodeid"))
            continue
        failure = node.find("failure")
        error = node.find("error")
        skipped = node.find("skipped")
        if failure is not None:
            result = result_stub(case, "FAIL", (failure.attrib.get("message") or "assert fallido")[:1000])
            result["failure_type"] = "funcional"
        elif error is not None:
            result = result_stub(case, "FAIL", (error.attrib.get("message") or "error de ejecución")[:1000])
            result["failure_type"] = "infraestructura"
        elif skipped is not None:
            result = result_stub(case, "SKIPPED", skipped.attrib.get("message", "Caso omitido"))
        else:
            result = result_stub(case, "PASS", "Sin observaciones")
        result["duration_seconds"] = round(float(node.attrib.get("time", "0")), 3)
        results.append(result)
    return results


def execute(
    selected: list[TestCase],
    selection: dict,
    *,
    run_id: str | None = None,
    requested_email: str = "",
    defer_final_status: bool = False,
) -> tuple[dict, int]:
    run_id = run_id or str(uuid.uuid4())
    started_at = iso_now()
    clock = perf_counter()
    run_dir = ROOT / "reports" / run_id
    run_dir.mkdir(parents=True, exist_ok=True)
    checks = run_checks()
    health = [check.__dict__ for check in checks]
    if not all(check.ok for check in checks):
        cases = [result_stub(case, "NOT RUN", "Preflight de IPAS falló") for case in selected]
        for case in cases:
            case["failure_type"] = "infraestructura"
        terminal_status = "FALLIDA"
        payload = {
            "run_id": run_id,
            "status": "EN CURSO" if defer_final_status else terminal_status,
            "test_status": terminal_status,
            "failure_type": "infraestructura",
            "started_at": started_at,
            "finished_at": iso_now(),
            "duration_seconds": round(perf_counter() - clock, 3),
            "selection": selection,
            "requested_email": requested_email,
            "health": health,
            "cases": cases,
        }
        (run_dir / "result.json").write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
        return payload, 2

    junit = run_dir / "junit.xml"
    html = run_dir / "pytest.html"
    command = [
        sys.executable,
        "-m",
        "pytest",
        *[case.nodeid for case in selected],
        "-v",
        f"--junitxml={junit}",
        f"--html={html}",
        "--self-contained-html",
        f"--run-id={run_id}",
    ]
    process = subprocess.run(command, cwd=ROOT, text=True, capture_output=True)
    (run_dir / "pytest.log").write_text(process.stdout + process.stderr, encoding="utf-8")
    cases = parse_junit(junit, selected) if junit.exists() else [
        result_stub(case, "NOT RUN", "pytest no generó JUnit") for case in selected
    ]
    failed = [case for case in cases if case["status"] == "FAIL"]
    not_run = [case for case in cases if case["status"] == "NOT RUN"]
    terminal_status = "FALLIDA" if failed or not_run else "FINALIZADA"
    payload = {
        "run_id": run_id,
        "status": "EN CURSO" if defer_final_status else terminal_status,
        "test_status": terminal_status,
        "failure_type": "funcional" if failed else ("infraestructura" if not_run else None),
        "started_at": started_at,
        "finished_at": iso_now(),
        "duration_seconds": round(perf_counter() - clock, 3),
        "selection": selection,
        "requested_email": requested_email,
        "health": health,
        "summary": {
            "total": len(cases),
            "pass": sum(case["status"] == "PASS" for case in cases),
            "fail": len(failed),
            "skipped": sum(case["status"] == "SKIPPED" for case in cases),
            "not_run": len(not_run),
        },
        "cases": cases,
    }
    (run_dir / "result.json").write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    return payload, 1 if failed or not_run else 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Runner trazable de IPAS QA")
    parser.add_argument("--suite", action="append", default=[])
    parser.add_argument("--case", action="append", dest="case_ids", default=[])
    parser.add_argument("--all", action="store_true", dest="all_cases")
    args = parser.parse_args()
    try:
        selected = Catalog().select(args.suite, args.case_ids, args.all_cases)
    except ValueError as exc:
        parser.error(str(exc))
    payload, exit_code = execute(
        selected,
        {"suites": args.suite, "case_ids": args.case_ids, "all": args.all_cases},
    )
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())

