"""Configuration for the Voice Agent CLI.

All user-facing settings live here. Edit these values to change
the agent's behaviour without touching the core code.
"""

from pathlib import Path

# ---------------------------------------------------------------------------
# LLM Backend
# ---------------------------------------------------------------------------
# Supported backends:
#   "ollama"   — free, local. Requires Ollama installed + running.
#   "openai"   — OpenAI API. Requires OPENAI_API_KEY env var.
#   "litellm"  — LiteLLM router. Requires OPENAI_API_KEY (or provider key).
#   "mock"     — returns a canned response. Good for testing the pipeline.
#   "custom"   — plug in your own implementation in llm.py.
LLM_BACKEND: str = "ollama"
LLM_MODEL: str = "llama3.2"          # model name (backend-specific)
OLLAMA_BASE_URL: str = "http://localhost:11434"

# ---------------------------------------------------------------------------
# TTS (Text-to-Speech)
# ---------------------------------------------------------------------------
# "edge-tts" — free, natural voices, needs internet (Microsoft Edge servers).
# "pyttsx3"  — fully offline, lower quality, no internet needed.
TTS_ENGINE: str = "edge-tts"

# edge-tts voice name (run `edge-tts --list-voices` to see all).
# Examples: en-US-JennyNeural, en-US-AriaNeural, en-GB-SoniaNeural
TTS_VOICE: str = "en-US-JennyNeural"

# pyttsx3 rate (words per minute) — only used when TTS_ENGINE == "pyttsx3"
TTS_RATE: int = 175

# ---------------------------------------------------------------------------
# STT (Speech-to-Text)
# ---------------------------------------------------------------------------
# "whisper"           — offline, high quality, heavier install (PyTorch).
# "speech_recognition" — online (Google Web Speech API), lighter, needs mic.
STT_ENGINE: str = "speech_recognition"

# Record timeout in seconds (how long to listen per turn).
RECORD_TIMEOUT: float = 10.0

# Silence threshold (seconds of silence before ending recording).
# Only used by speech_recognition mode.
SILENCE_TIMEOUT: float = 3.0

# ---------------------------------------------------------------------------
# CLI behaviour
# ---------------------------------------------------------------------------
# When True, print the transcribed text and LLM response to the console
# in addition to speaking them.
VERBOSE: bool = True

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
PROJECT_ROOT: Path = Path(__file__).resolve().parent.parent
