"""Main agent loop — the heart of the voice agent.

The loop is simple:

    1. Listen  (STT → text)
    2. Think   (LLM → answer text)
    3. Speak   (TTS ← answer text)
    4. Repeat

Exit with Ctrl+C at any time.
"""

from __future__ import annotations

import asyncio
import sys

from colorama import Fore, Style, init as colorama_init

from .config import VERBOSE
from .llm import ask_llm, create_llm
from .stt import transcribe
from .tts import speak

# Initialize colorama for cross-platform coloured console output.
colorama_init(autoreset=True)


def _print(text: str, color: str = Fore.WHITE) -> None:
    if not VERBOSE:
        return
    print(color + text + Style.RESET_ALL, flush=True)


class VoiceAgent:
    """Orchestrates the listen → think → speak loop."""

    def __init__(self, llm_backend: str = "", llm_model: str = ""):
        self.llm = create_llm(backend=llm_backend, model=llm_model)
        self._recognizer = None

    # ------------------------------------------------------------------
    # One turn
    # ------------------------------------------------------------------

    async def run_turn(self) -> bool:
        """Run a single listen → think → speak cycle.

        Returns True when the turn completed normally, False when the
        user wants to exit (empty input, keyboard interrupt, etc.).
        """
        # 1. Listen
        text = transcribe(recognizer=self._recognizer)
        if not text:
            print(
                Fore.YELLOW
                + "  (Nothing heard — try again, or press Ctrl+C to exit)"
                + Style.RESET_ALL,
                flush=True,
            )
            return True

        # 2. Think
        _print(f"\n  🤔 Thinking...", Fore.CYAN)
        response = ask_llm(self.llm, text)
        answer = response.text.strip()

        _print(f"\n  💡 {response.backend.upper()} ({response.model}):", Fore.CYAN)
        _print(f"     {answer}", Fore.GREEN)

        if not answer:
            _print("  (Empty response — skipping speech)", Fore.YELLOW)
            return True

        # 3. Speak
        print("  🔊 Speaking...", flush=True)
        await speak(answer)
        print(f"  ✅ Done{Fore.RESET}", flush=True)

        return True

    # ------------------------------------------------------------------
    # Main loop
    # ------------------------------------------------------------------

    async def run(self) -> None:
        """Start the continuous voice conversation loop."""
        print()
        print("=" * 60)
        print(f"  🎙️  Voice Agent CLI  |  Backend: {self.llm.__class__.__name__}")
        print("  Speak when prompted — Ctrl+C to exit")
        print("=" * 60)
        print()

        try:
            while True:
                await self.run_turn()
                print()
        except KeyboardInterrupt:
            print(
                f"\n{Fore.YELLOW}  👋  Exiting...{Style.RESET_ALL}",
                flush=True,
            )
