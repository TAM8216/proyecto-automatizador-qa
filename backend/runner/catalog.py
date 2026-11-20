from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import yaml

from backend.config import ROOT


CATALOG_PATH = ROOT / "config" / "test_catalog.yaml"


@dataclass(frozen=True)
class TestCase:
    id: str
    name: str
    type: str
    module: str
    priority: str
    suites: tuple[str, ...]
    nodeid: str | None
    engine: str = "pytest"
    controlled_fail: bool = False
    defect: str | None = None


class Catalog:
    def __init__(self, path: Path = CATALOG_PATH):
        raw = yaml.safe_load(path.read_text(encoding="utf-8"))
        self.version = raw["version"]
        self.flows = raw.get("flows", {})
        self.suites = raw["suites"]
        unknown_flows = {
            metadata.get("flow")
            for metadata in self.suites.values()
            if metadata.get("flow") not in self.flows
        }
        if unknown_flows:
            raise ValueError(f"El catálogo contiene flujos desconocidos: {sorted(unknown_flows)}")
        self.cases = tuple(
            TestCase(
                id=item["id"],
                name=item["name"],
                type=item["type"],
                module=item["module"],
                priority=item["priority"],
                suites=tuple(item["suites"]),
                nodeid=item.get("nodeid"),
                engine=item.get("engine", "pytest"),
                controlled_fail=bool(item.get("controlled_fail", False)),
                defect=item.get("defect"),
            )
            for item in raw["cases"]
        )
        ids = [case.id for case in self.cases]
        if len(ids) != len(set(ids)):
            raise ValueError("El catálogo contiene IDs duplicados.")

    def select(
        self,
        suites: list[str],
        case_ids: list[str],
        all_cases: bool,
        test_type: str | None = None,
    ) -> list[TestCase]:
        unknown_suites = set(suites) - set(self.suites)
        if unknown_suites:
            raise ValueError(f"Suites desconocidas: {sorted(unknown_suites)}")
        known_ids = {case.id for case in self.cases}
        unknown_cases = set(case_ids) - known_ids
        if unknown_cases:
            raise ValueError(f"Casos desconocidos: {sorted(unknown_cases)}")
        if all_cases:
            selected = [
                case for case in self.cases
                if test_type is None or self._case_type(case) == test_type
            ]
        else:
            selected = [
                case
                for case in self.cases
                if (case.id in case_ids or any(suite in case.suites for suite in suites))
                and (test_type is None or self._case_type(case) == test_type)
            ]
        if not selected:
            raise ValueError("Selecciona --suite, --case o --all.")
        return selected

    def _case_type(self, case: TestCase) -> str:
        return "no_funcional" if case.engine == "locust" else "funcional"

