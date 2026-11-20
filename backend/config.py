from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from pydantic import Field, HttpUrl, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


ROOT = Path(__file__).resolve().parents[1]
SAFE_QA_DATABASE = "ius_puniendi_qa"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=ROOT / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    sut_frontend_url: HttpUrl = "http://127.0.0.1:3000"
    sut_api_url: HttpUrl = "http://127.0.0.1:4000/api"
    sut_ia_url: HttpUrl = "http://127.0.0.1:8001"

    qa_db_host: str = "127.0.0.1"
    qa_db_port: int = 5432
    qa_db_name: str = SAFE_QA_DATABASE
    qa_db_user: str = "postgres"
    qa_db_password: str = Field(default="", repr=False)

    qa_superadmin_email: str = "qa.superadmin@ipas.test"
    qa_superadmin_password: str = Field(default="", repr=False)
    qa_admin_email: str = "qa.admin@ipas.test"
    qa_admin_password: str = Field(default="", repr=False)
    qa_abogado_email: str = "qa.abogado@ipas.test"
    qa_abogado_password: str = Field(default="", repr=False)

    qa_browser: str = "edge"
    qa_headless: bool = False
    qa_wait_seconds: int = 15

    smtp_host: str = ""
    smtp_port: int = 587
    smtp_user: str = ""
    smtp_password: str = Field(default="", repr=False)
    smtp_from: str = ""
    smtp_use_starttls: bool = True
    smtp_timeout_seconds: int = 20

    qa_load_users: int = 5
    qa_load_spawn_rate: float = 1.0
    qa_load_duration_seconds: int = 30
    qa_load_p95_limit_ms: float = 2000.0
    qa_load_error_rate_limit: float = 0.01

    anthropic_api_key: str = Field(default="", repr=False)
    anthropic_model: str = "claude-sonnet-5-5"
    anthropic_api_url: HttpUrl = "https://api.anthropic.com/v1/messages"
    anthropic_api_version: str = "2026-10-21"
    anthropic_timeout_seconds: int = 60

    ai_provider: str = "groq"
    groq_api_key: str = Field(default="", repr=False)
    groq_model: str = "openai/gpt-oss-120b"
    groq_api_url: HttpUrl = "https://api.groq.com/openai/v1/chat/completions"
    groq_timeout_seconds: int = 60

    @model_validator(mode="after")
    def reject_non_qa_database(self) -> "Settings":
        if self.qa_db_name.strip().lower() != SAFE_QA_DATABASE:
            raise ValueError(
                f"Ejecución bloqueada: QA_DB_NAME debe ser exactamente {SAFE_QA_DATABASE!r}."
            )
        return self

    @property
    def db_kwargs(self) -> dict[str, object]:
        return {
            "host": self.qa_db_host,
            "port": self.qa_db_port,
            "dbname": self.qa_db_name,
            "user": self.qa_db_user,
            "password": self.qa_db_password,
        }

    @property
    def smtp_configured(self) -> bool:
        return bool(self.smtp_host.strip() and self.smtp_from.strip())

    @property
    def smtp_auth_ascii(self) -> bool:
        return self.smtp_user.isascii() and self.smtp_password.isascii()

    @property
    def smtp_password_for_auth(self) -> str:
        if self.smtp_host.strip().lower() in {"smtp.gmail.com", "smtp.googlemail.com"}:
            return "".join(self.smtp_password.split())
        return self.smtp_password

    @property
    def smtp_credentials_valid(self) -> bool:
        if not self.smtp_auth_ascii:
            return False
        if self.smtp_host.strip().lower() in {"smtp.gmail.com", "smtp.googlemail.com"} and self.smtp_user:
            return len(self.smtp_password_for_auth) == 16
        return True

    @property
    def smtp_ready(self) -> bool:
        return self.smtp_configured and self.smtp_credentials_valid

    @property
    def anthropic_configured(self) -> bool:
        return bool(self.anthropic_api_key.strip())

    @property
    def groq_configured(self) -> bool:
        return bool(self.groq_api_key.strip())


@lru_cache
def get_settings() -> Settings:
    return Settings()

