"""LLM backends — the "thinking" part of the agent.

Supports multiple backends through a common interface:

    Ollama      — free, local LLM runtime.
    OpenAI      — OpenAI's API (requires OPENAI_API_KEY).
    LiteLLM     — unified API that routes to many providers.
    Mock        — returns canned responses (testing only).
    Custom      — subclass BaseLLM and plug in your own backend.

Set LLM_BACKEND in config.py to choose which one the agent uses.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional

from pydantic import BaseModel, Field

from .config import LLM_BACKEND, LLM_MODEL, OLLAMA_BASE_URL


# ---------------------------------------------------------------------------
# Shared types
# ---------------------------------------------------------------------------

class LLMResponse(BaseModel):
    """Normalised response from any backend."""

    text: str
    model: str = ""
    backend: str = ""


# ---------------------------------------------------------------------------
# Base class
# ---------------------------------------------------------------------------

class BaseLLM(ABC):
    """Every backend implements `ask(question) -> LLMResponse`."""

    @abstractmethod
    def ask(self, question: str, system: Optional[str] = None) -> LLMResponse:
        """Send *question* to the LLM and return the answer."""


# ---------------------------------------------------------------------------
# Ollama backend (free, local)
# ---------------------------------------------------------------------------

class OllamaLLM(BaseLLM):
    """Talks to a local Ollama instance."""

    def __init__(self, model: str = "llama3.2", base_url: str = OLLAMA_BASE_URL):
        self.model = model
        self.base_url = base_url.rstrip("/")
        self._client = None

    def _get_client(self):
        if self._client is None:
            import ollama as _ollama  # lazy import

            self._client = _ollama
        return self._client

    def ask(self, question: str, system: Optional[str] = None) -> LLMResponse:
        client = self._get_client()
        messages: list[dict[str, str]] = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": question})

        resp = client.chat(
            model=self.model,
            messages=messages,
            stream=False,
        )
        text = resp["message"]["content"]
        return LLMResponse(text=text, model=self.model, backend="ollama")


# ---------------------------------------------------------------------------
# OpenAI backend
# ---------------------------------------------------------------------------

class OpenAILLM(BaseLLM):
    """Uses OpenAI's REST API."""

    def __init__(self, model: str = "gpt-4o-mini"):
        self.model = model

    def ask(self, question: str, system: Optional[str] = None) -> LLMResponse:
        import openai  # lazy import

        client = openai.OpenAI()
        messages: list[dict[str, str]] = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": question})

        resp = client.chat.completions.create(
            model=self.model,
            messages=messages,
            stream=False,
        )
        text = resp.choices[0].message.content or ""
        return LLMResponse(text=text, model=self.model, backend="openai")


# ---------------------------------------------------------------------------
# LiteLLM backend — one API for many providers
# ---------------------------------------------------------------------------

class LiteLLM(BaseLLM):
    """Uses LiteLLM to route to any supported provider."""

    def __init__(self, model: str = "gpt-4o-mini"):
        self.model = model

    def ask(self, question: str, system: Optional[str] = None) -> LLMResponse:
        from litellm import completion  # lazy import

        messages: list[dict[str, str]] = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": question})

        resp = completion(
            model=self.model,
            messages=messages,
            stream=False,
        )
        text = resp["choices"][0]["message"]["content"] or ""
        return LLMResponse(text=text, model=self.model, backend="litellm")


# ---------------------------------------------------------------------------
# Mock backend — returns a canned response (useful for testing the pipeline)
# ---------------------------------------------------------------------------

class MockLLM(BaseLLM):
    """Always returns the same helpful-sounding response."""

    def ask(self, question: str, system: Optional[str] = None) -> LLMResponse:
        return LLMResponse(
            text=(
                "This is a mock response from the Voice Agent CLI. "
                "The pipeline is working — STT captured your question "
                f"('{question[:40]}...'), but no real LLM backend is "
                "configured yet. Set LLM_BACKEND in config.py to "
                "'ollama', 'openai', or 'litellm' to get real answers."
            ),
            model="mock",
            backend="mock",
        )


# ---------------------------------------------------------------------------
# Factory
# ---------------------------------------------------------------------------

SYSTEM_PROMPT = (
    "You are a helpful voice assistant. Keep your answers concise and "
    "conversational — the user is listening, not reading. Aim for 2-4 "
    "sentences unless the question clearly needs more detail."
)


def create_llm(
    backend: str = LLM_BACKEND,
    model: str = LLM_MODEL,
) -> BaseLLM:
    """Instantiate the right backend based on *backend*."""
    backends: dict[str, type[BaseLLM]] = {
        "ollama": OllamaLLM,
        "openai": OpenAILLM,
        "litellm": LiteLLM,
        "mock": MockLLM,
    }

    cls = backends.get(backend)
    if cls is None:
        raise ValueError(
            f"Unknown LLM backend '{backend}'. "
            f"Choose from: {', '.join(backends.keys())}"
        )

    if backend == "ollama":
        return cls(model=model)
    if backend == "openai":
        return cls(model=model)
    if backend == "litellm":
        return cls(model=model)
    # mock takes no constructor args
    return cls()


def ask_llm(llm: BaseLLM, question: str) -> LLMResponse:
    """Convenience wrapper that passes the shared system prompt."""
    return llm.ask(question, system=SYSTEM_PROMPT)
