from __future__ import annotations

import httpx
import pytest

from backend.ai.provider import AIConfigurationError, AnthropicProvider, GroqProvider, get_ai_provider
from backend.config import Settings


def build_settings(**overrides) -> Settings:
    values = {"_env_file": None, "qa_db_name": "ius_puniendi_qa", **overrides}
    return Settings(**values)


def test_factory_selecciona_groq_por_configuracion():
    provider = get_ai_provider(build_settings(ai_provider="groq", groq_api_key="clave-de-prueba"))
    assert isinstance(provider, GroqProvider)


def test_factory_conserva_anthropic_como_alternativa():
    provider = get_ai_provider(build_settings(ai_provider="anthropic", anthropic_api_key="clave-de-prueba"))
    assert isinstance(provider, AnthropicProvider)


def test_factory_rechaza_proveedor_desconocido():
    with pytest.raises(AIConfigurationError, match="AI_PROVIDER"):
        get_ai_provider(build_settings(ai_provider="desconocido"))


def test_groq_envia_json_y_normaliza_metadatos(monkeypatch):
    observed = {}

    def fake_post(url, *, headers, json, timeout):
        observed.update({"url": url, "headers": headers, "json": json, "timeout": timeout})
        return httpx.Response(
            200,
            headers={"x-request-id": "req-test"},
            json={
                "model": "openai/gpt-oss-120b",
                "choices": [{"message": {"content": '{"ready": true}'}, "finish_reason": "stop"}],
                "usage": {"prompt_tokens": 10, "completion_tokens": 3},
            },
            request=httpx.Request("POST", url),
        )

    monkeypatch.setattr(httpx, "post", fake_post)
    provider = GroqProvider(build_settings(groq_api_key="clave-de-prueba"))
    response = provider.complete_json("sistema", "entrada")

    assert response.payload == {"ready": True}
    assert response.metadata["provider"] == "groq"
    assert observed["url"].endswith("/chat/completions")
    assert observed["headers"]["Authorization"] == "Bearer clave-de-prueba"
    assert observed["json"]["response_format"] == {"type": "json_object"}
