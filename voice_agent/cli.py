"""Entry point for ``python -m voice_agent`` and the ``voice-agent`` CLI.

Usage
-----
python -m voice_agent
python -m voice_agent --backend ollama --model llama3.2
python -m voice_agent --verbose
"""

from __future__ import annotations

import argparse
import sys

from .agent import VoiceAgent


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="voice-agent",
        description="Free, local voice assistant — listen, think, speak.",
    )
    parser.add_argument(
        "--backend",
        choices=["ollama", "openai", "litellm", "mock"],
        help="LLM backend (overrides config.py)",
    )
    parser.add_argument(
        "--model",
        help="Model name for the chosen backend (overrides config.py)",
    )
    parser.add_argument(
        "--voice",
        help="TTS voice name (overrides config.py TTS_VOICE)",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Print full transcripts and responses to console",
    )
    args = parser.parse_args(argv)

    backend = args.backend or ""
    model = args.model or ""

    agent = VoiceAgent(llm_backend=backend, llm_model=model)
    asyncio.run(agent.run())
    return 0


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
