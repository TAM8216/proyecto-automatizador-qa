from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any, Protocol

import httpx

from backend.config import Settings, get_settings


class AIConfigurationError(RuntimeError):
    pass


class AIProviderError(RuntimeError):
    pass


@dataclass(frozen=True)
class AIResponse:
    payload: dict[str, Any]
    metadata: dict[str, Any]


class AIProvider(Protocol):
    def complete_json(self, system: str, prompt: str) -> AIResponse: ...


def _parse_json(text: str) -> dict[str, Any]:
    cleaned = text.strip()
    if cleaned.startswith("```"):
        lines = cleaned.splitlines()
        cleaned = "\n".join(lines[1:-1]).strip()
    try:
        payload = json.loads(cleaned)
    except json.JSONDecodeError as exc:
        raise AIProviderError("Anthropic devolvió una respuesta que no es JSON válido.") from exc
    if not isinstance(payload, dict):
        raise AIProviderError("Anthropic debe devolver un objeto JSON.")
    return payload


class AnthropicProvider:
    def __init__(self, settings: Settings | None = None):
        self.settings = settings or get_settings()

    def complete_json(self, system: str, prompt: str) -> AIResponse:
        if not self.settings.anthropic_configured:
            raise AIConfigurationError(
                "ANTHROPIC_API_KEY no está configurada. Agrégala al .env local para usar la IA real."
            )
        headers = {
            "x-api-key": self.settings.anthropic_api_key,
            "anthropic-version": self.settings.anthropic_api_version,
            "content-type": "application/json",
        }
        body = {
            "model": self.settings.anthropic_model,
            "max_tokens": 4096,
            "system": system,
            "messages": [{"role": "user", "content": prompt}],
        }
        try:
            response = httpx.post(
                str(self.settings.anthropic_api_url),
                headers=headers,
                json=body,
                timeout=self.settings.anthropic_timeout_seconds,
            )
            response.raise_for_status()
            raw = response.json()
        except (httpx.HTTPError, ValueError) as exc:
            status_code = getattr(getattr(exc, "response", None), "status_code", None)
            suffix = f" (HTTP {status_code})" if status_code else ""
            raise AIProviderError(f"No se pudo completar la solicitud a Anthropic{suffix}.") from exc

        text = "".join(
            block.get("text", "")
            for block in raw.get("content", [])
            if block.get("type") == "text"
        )
        return AIResponse(
            payload=_parse_json(text),
            metadata={
                "provider": "anthropic",
                "model": raw.get("model", self.settings.anthropic_model),
                "request_id": response.headers.get("request-id"),
                "usage": raw.get("usage", {}),
                "stop_reason": raw.get("stop_reason"),
            },
        )


class GroqProvider:
    def __init__(self, settings: Settings | None = None):
        self.settings = settings or get_settings()

    def complete_json(self, system: str, prompt: str) -> AIResponse:
        if not self.settings.groq_configured:
            raise AIConfigurationError(
                "GROQ_API_KEY no está configurada. Agrégala al .env local o inyéctala al iniciar la API."
            )
        headers = {
            "Authorization": f"Bearer {self.settings.groq_api_key}",
            "Content-Type": "application/json",
        }
        body = {
            "model": self.settings.groq_model,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": prompt},
            ],
            "response_format": {"type": "json_object"},
            "temperature": 0.1,
            "max_completion_tokens": 4096,
        }
        try:
            response = httpx.post(
                str(self.settings.groq_api_url),
                headers=headers,
                json=body,
                timeout=self.settings.groq_timeout_seconds,
            )
            response.raise_for_status()
            raw = response.json()
            text = raw["choices"][0]["message"]["content"]
        except (httpx.HTTPError, KeyError, IndexError, TypeError, ValueError) as exc:
            status_code = getattr(getattr(exc, "response", None), "status_code", None)
            suffix = f" (HTTP {status_code})" if status_code else ""
            raise AIProviderError(f"No se pudo completar la solicitud a Groq{suffix}.") from exc
        return AIResponse(
            payload=_parse_json(text),
            metadata={
                "provider": "groq",
                "model": raw.get("model", self.settings.groq_model),
                "request_id": response.headers.get("x-request-id"),
                "usage": raw.get("usage", {}),
                "finish_reason": raw.get("choices", [{}])[0].get("finish_reason"),
            },
        )


def get_ai_provider(settings: Settings | None = None) -> AIProvider:
    current = settings or get_settings()
    provider = current.ai_provider.strip().lower()
    if provider == "groq":
        return GroqProvider(current)
    if provider == "anthropic":
        return AnthropicProvider(current)
    raise AIConfigurationError("AI_PROVIDER debe ser 'groq' o 'anthropic'.")
