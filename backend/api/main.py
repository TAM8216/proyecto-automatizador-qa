from __future__ import annotations

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from backend.api import service
from backend.ai import service as ai_service
from backend.ai.provider import AIConfigurationError, AIProviderError
from backend.api.schemas import AIAnalyzeRequest, AIGenerateRequest, AIReviewRequest, RunAccepted, RunCreate
from backend.config import get_settings
from backend.runner.catalog import Catalog


app = FastAPI(
    title="IPAS QA Platform API",
    description="Orquestador de pruebas automatizadas contra el ambiente local QA de IPAS.",
    version="0.5.0",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)


@app.get("/health")
async def api_health() -> dict[str, str]:
    return {"status": "ok", "service": "qa-platform-api"}


@app.get("/suites")
async def get_suites() -> dict:
    catalog = Catalog()
    settings = get_settings()
    return {
        "version": catalog.version,
        "types": [
            {"id": "funcional", "name": "Funcionales", "available": True},
            {"id": "no_funcional", "name": "No funcionales", "available": True},
        ],
        "flows": [
            {"id": flow_id, **metadata}
            for flow_id, metadata in catalog.flows.items()
        ],
        "delivery": {
            "smtp_configured": settings.smtp_configured,
            "smtp_ready": settings.smtp_ready,
            "message": (
                "SMTP listo para entregar reportes."
                if settings.smtp_ready
                else "Configura SMTP_HOST y SMTP_FROM con credenciales ASCII y reinicia la API."
            ),
        },
        "suites": [
            {
                "id": suite_id,
                **metadata,
                "type": metadata.get("type", "funcional"),
                "cases": [
                    {
                        "id": case.id,
                        "name": case.name,
                        "type": case.type,
                        "module": case.module,
                        "priority": case.priority,
                        "controlled_fail": case.controlled_fail,
                    }
                    for case in catalog.cases
                    if suite_id in case.suites
                ],
            }
            for suite_id, metadata in catalog.suites.items()
        ],
    }


@app.post("/runs", response_model=RunAccepted, status_code=status.HTTP_202_ACCEPTED)
async def create_run(payload: RunCreate, request: Request) -> RunAccepted:
    try:
        selected = service.select_cases(payload)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    run_id, selection, _ = service.create_pending_run(payload, selected)
    service.enqueue_run(run_id, selected, selection, str(payload.email))
    return RunAccepted(
        run_id=run_id,
        status="PENDIENTE",
        status_url=str(request.url_for("get_run", run_id=run_id)),
    )


@app.get("/runs/{run_id}", name="get_run")
async def get_run(run_id: str) -> dict:
    payload = service.read_result(run_id)
    if payload is None:
        raise HTTPException(status_code=404, detail="Corrida no encontrada.")
    return payload


@app.get("/runs/{run_id}/reports/{report_format}")
async def download_report(run_id: str, report_format: str):
    filenames = {
        "docx": ("informe_detallado.docx", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"),
        "html": ("reporte_autocontenido.html", "text/html; charset=utf-8"),
    }
    if report_format not in filenames:
        raise HTTPException(status_code=404, detail="Formato de reporte desconocido.")
    filename, media_type = filenames[report_format]
    path = service.RUNS_ROOT / run_id / filename
    if not path.is_file():
        raise HTTPException(status_code=404, detail="Reporte no disponible.")
    return FileResponse(path, media_type=media_type, filename=filename)


def _raise_ai_error(exc: Exception) -> None:
    if isinstance(exc, AIConfigurationError):
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    if isinstance(exc, (ValueError, FileNotFoundError)):
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    if isinstance(exc, AIProviderError):
        raise HTTPException(status_code=502, detail=str(exc)) from exc
    raise exc


@app.post("/ai/analyses")
async def analyze_requirement(payload: AIAnalyzeRequest) -> dict:
    try:
        return ai_service.analyze(payload.requirement, payload.source_type)
    except Exception as exc:
        _raise_ai_error(exc)


@app.post("/ai/drafts")
async def generate_draft(payload: AIGenerateRequest) -> dict:
    try:
        return ai_service.generate(payload.analysis_id, payload.clarifications)
    except Exception as exc:
        _raise_ai_error(exc)


@app.get("/ai/analyses/{analysis_id}")
async def get_ai_analysis(analysis_id: str) -> dict:
    try:
        return ai_service.get_record(analysis_id)
    except Exception as exc:
        _raise_ai_error(exc)


@app.post("/ai/analyses/{analysis_id}/review")
async def review_ai_draft(analysis_id: str, payload: AIReviewRequest) -> dict:
    try:
        return ai_service.review(analysis_id, payload.approved, payload.reviewer, payload.corrections)
    except Exception as exc:
        _raise_ai_error(exc)


@app.post("/ai/runs/{run_id}/summary")
async def summarize_run_failures(run_id: str) -> dict:
    try:
        return ai_service.summarize_failures(run_id, service.RUNS_ROOT / run_id)
    except Exception as exc:
        _raise_ai_error(exc)

