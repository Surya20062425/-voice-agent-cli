"""Text-to-Speech — speaks the agent's responses aloud.

Supports two engines:

    edge-tts  — free, natural Microsoft Edge voices. Needs internet.
    pyttsx3   — fully offline, lower quality. No internet needed.

Set TTS_ENGINE in config.py to choose.
"""

from typing import Optional

import edge_tts
import pyttsx3

from .config import TTS_ENGINE, TTS_VOICE, TTS_RATE


async def speak(text: str, voice: Optional[str] = None) -> None:
    """Speak *text* aloud using the configured TTS engine.

    When *voice* is given it overrides the configured default for this
    call only (useful for per-response voice selection).
    """
    engine = voice or TTS_VOICE

    if TTS_ENGINE == "edge-tts":
        await _edge_speak(text, engine)
    elif TTS_ENGINE == "pyttsx3":
        _pyttsx3_speak(text, engine)
    else:
        raise ValueError(f"Unknown TTS engine: {TTS_ENGINE}")


async def _edge_speak(text: str, voice: str) -> None:
    """edge-tts implementation — asynchronous, streaming to speakers."""
    communicate = edge_tts.Communicate(text, voice)
    await communicate.stream()


def _pyttsx3_speak(text: str, voice_name: str) -> None:
    """pyttsx3 implementation — synchronous, fully offline."""
    engine = pyttsx3.init()
    engine.setProperty("rate", TTS_RATE)

    # Try to pick a matching voice by name (best-effort).
    voices = engine.getProperty("voices")
    for v in voices:
        if voice_name.lower() in v.id.lower():
            engine.setProperty("voice", v.id)
            break

    engine.say(text)
    engine.runAndWait()


def list_edge_voices() -> list[str]:
    """Return the names of all available edge-tts voices."""
    return list(edge_tts.VOICES)
