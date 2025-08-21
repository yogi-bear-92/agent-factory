"""Azure AI Foundry (Azure OpenAI) integration helpers.

Provides a thin wrapper to create an Azure OpenAI client and a simple
chat helper. Prefers environment-driven configuration via pydantic
settings (see `src/config/settings.py`).
"""
from __future__ import annotations

import os
from typing import Any, Dict, List, Optional

try:
    # New OpenAI Python SDK (>=1.x)
    from openai import AzureOpenAI
except Exception:  # pragma: no cover - optional dependency
    AzureOpenAI = None  # type: ignore

from config.settings import settings


def get_azure_openai_client() -> AzureOpenAI:
    """Create and return an Azure OpenAI client using settings or environment.

    Requires the `openai` package (>=1.0) and sets up the client for
    Azure endpoints.
    """
    if AzureOpenAI is None:
        raise RuntimeError(
            "openai package not installed. Please add 'openai>=1.0' to dependencies."
        )

    endpoint = settings.azure_openai.endpoint or os.getenv("AZURE_OPENAI_ENDPOINT", "")
    api_key = settings.azure_openai.api_key or os.getenv("AZURE_OPENAI_API_KEY", "")
    api_version = (
        settings.azure_openai.api_version
        or os.getenv("AZURE_OPENAI_API_VERSION", "2024-05-01-preview")
    )

    if not endpoint:
        raise ValueError(
            "AZURE_OPENAI_ENDPOINT is not set. Configure it in .env or environment."
        )

    # Prefer API key auth for simplicity
    if not api_key and not settings.azure_openai.use_aad:
        raise ValueError(
            "AZURE_OPENAI_API_KEY is not set. Provide key or set use_aad=true."
        )

    client = AzureOpenAI(
        azure_endpoint=endpoint,
        api_key=api_key if api_key else None,
        api_version=api_version,
    )
    return client


def chat_completion(
    messages: List[Dict[str, str]],
    *,
    deployment: Optional[str] = None,
    temperature: Optional[float] = None,
    max_tokens: Optional[int] = None,
) -> str:
    """Perform a chat completion call against Azure OpenAI.

    Args:
        messages: List of {"role": "system|user|assistant", "content": "..."}
        deployment: Optional Azure deployment name (falls back to settings)
        temperature: Sampling temperature
        max_tokens: Max tokens to generate

    Returns:
        Assistant message content as string.
    """
    client = get_azure_openai_client()
    deployment_name = (
        deployment
        or settings.azure_openai.deployment
        or os.getenv("AZURE_OPENAI_DEPLOYMENT", "")
    )
    if not deployment_name:
        raise ValueError(
            "AZURE_OPENAI_DEPLOYMENT is not set. Configure deployment name in .env."
        )

    resp = client.chat.completions.create(
        model=deployment_name,
        messages=messages,
        temperature=temperature if temperature is not None else settings.llm.temperature,
        max_tokens=max_tokens if max_tokens is not None else settings.llm.max_tokens,
    )
    return resp.choices[0].message.content or ""
