from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, EmailStr, Field, model_validator


class RunCreate(BaseModel):
    email: EmailStr
    type: Literal["funcional", "no_funcional"] = "funcional"
    suite: str | None = None
    case_ids: list[str] = Field(default_factory=list)
    all_cases: bool = False
    users: int = Field(default=5, ge=1, le=50)
    spawn_rate: float = Field(default=1.0, gt=0, le=10)
    duration_seconds: int = Field(default=30, ge=10, le=600)

    @model_validator(mode="after")
    def validate_selection(self) -> "RunCreate":
        if not self.suite and not self.case_ids and not self.all_cases:
            raise ValueError("Selecciona suite, casos específicos o all_cases=true.")
        return self


class RunAccepted(BaseModel):
    run_id: str
    status: Literal["PENDIENTE"]
    status_url: str


class AIAnalyzeRequest(BaseModel):
    requirement: str = Field(min_length=20, max_length=20_000)
    source_type: Literal["requisito", "caso_prueba"] = "requisito"


class AIGenerateRequest(BaseModel):
    analysis_id: str
    clarifications: dict[str, str] = Field(default_factory=dict)


class AIReviewRequest(BaseModel):
    approved: bool
    reviewer: str = Field(default="Usuario", min_length=2, max_length=120)
    corrections: list[str] = Field(default_factory=list, max_length=100)

