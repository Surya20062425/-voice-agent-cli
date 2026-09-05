"""Speech-to-Text — transcribes your voice into text.

Supports two engines:

    speech_recognition — uses Google's free Web Speech API (online).
                         Lightweight, works with any microphone.
    whisper            — OpenAI Whisper, fully offline, higher quality.
                         Needs PyTorch + the whisper package installed.

Set STT_ENGINE in config.py to choose.
"""

from typing import Optional

import speech_recognition as sr

from .config import RECORD_TIMEOUT, SILENCE_TIMEOUT, STT_ENGINE


def transcribe(recognizer: Optional["sr.Recognizer"] = None) -> str:
    """Listen to the microphone and return the transcribed text.

    When *recognizer* is passed in it is reused (avoids re-creation
    on every turn).  Returns an empty string when nothing was said or
    the engine is unavailable.
    """
    if STT_ENGINE == "speech_recognition":
        return _speech_recognition_transcribe(recognizer)
    if STT_ENGINE == "whisper":
        return _whisper_transcribe()
    raise ValueError(f"Unknown STT engine: {STT_ENGINE}")


# ---------------------------------------------------------------------------
# speech_recognition backend
# ---------------------------------------------------------------------------

def _speech_recognition_transcribe(
    recognizer: Optional["sr.Recognizer"] = None,
) -> str:
    """Use Google's free Web Speech API via the SpeechRecognition lib."""
    r = recognizer or sr.Recognizer()
    mic = sr.Microphone()

    with mic:
        r.adjust_for_ambient_noise(mic, duration=1)

    print("  🎤 Listening... (speak now)", flush=True)

    with mic:
        try:
            audio = r.listen(mic, timeout=RECORD_TIMEOUT, phrase_time_limit=30)
        except sr.WaitTimeoutError:
            print("  ⏱️  No speech detected (timeout)", flush=True)
            return ""

    try:
        text = r.recognize_google(audio)
        print(f"  📝 Heard: {text}", flush=True)
        return text
    except sr.UnknownValueError:
        print("  🤷  Could not understand audio", flush=True)
        return ""
    except sr.RequestError as exc:
        print(f"  ⚠️  Speech recognition service error: {exc}", flush=True)
        return ""


# ---------------------------------------------------------------------------
# whisper backend (optional — only if openai-whisper is installed)
# ---------------------------------------------------------------------------

def _whisper_transcribe() -> str:
    """Use OpenAI Whisper for offline transcription.

    This is a placeholder that tries to import whisper at call time so
    the package is only required when STT_ENGINE == "whisper".
    """
    try:
        import whisper  # type: ignore[import-untyped]
    except ImportError as exc:
        print(
            "  ⚠️  whisper not installed. Run: pip install openai-whisper",
            flush=True,
        )
        return ""

    print("  🎤 Listening... (Whisper — speak now)", flush=True)

    try:
        import pyaudio  # noqa: F401  # needed for Microphone capture below
        import wave
    except ImportError:
        print(
            "  ⚠️  pyaudio not available for Whisper input. "
            "Install with: pip install pyaudio",
            flush=True,
        )
        return ""

    # Record raw audio from mic into an in-memory WAV, then hand it to
    # Whisper.  This mirrors what SpeechRecognition does internally.
    import io

    pa = pyaudio.PyAudio()
    stream = pa.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=16000,
        input=True,
        frames_per_buffer=1024,
    )

    frames: list[bytes] = []
    try:
        for _ in range(int(16000 / 1024 * RECORD_TIMEOUT)):
            data = stream.read(1024, exception_on_overflow=False)
            frames.append(data)
    except KeyboardInterrupt:
        pass
    finally:
        stream.stop_stream()
        stream.close()
        pa.terminate()

    buf = io.BytesIO()
    with wave.open(buf, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)  # paInt16 → 2 bytes
        wf.setframerate(16000)
        wf.writeframes(b"".join(frames))

    buf.seek(0)

    model = whisper.load_model("base")  # "tiny" is faster but less accurate
    result = model.transcribe(buf)
    text = result["text"].strip()

    if text:
        print(f"  📝 Heard: {text}", flush=True)
    else:
        print("  🤷  Could not understand audio", flush=True)

    return text
