# Voice Agent CLI — Free, Local, All-in-One

A command-line voice agent that listens, thinks, and speaks — entirely free, running locally on your machine.

**Listen** (STT): Whisper / SpeechRecognition → your voice becomes text  
**Think** (LLM): Configurable backend with free defaults — answers any question  
**Speak** (TTS): edge-tts → natural-sounding speech, no API key required

No subscriptions. No cloud. No API keys for core features.

---

## Quick Start

```bash
# 1. Clone
git clone https://github.com/Surya20062425/voice-agent-cli.git
cd voice-agent-cli

# 2. Set up virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run
python -m voice_agent
```

Speak when prompted — the agent listens, answers, and speaks back. Press `Ctrl+C` to exit.

---

## What It Does

| Feature | How | Cost |
|---|---|---|
| **Speech-to-Text** | Whisper (offline) or SpeechRecognition (online) | Free |
| **Text-to-Speech** | edge-tts (Microsoft Edge's free TTS) | Free, no key |
| **LLM Backend** | Configurable — OpenAI, Ollama, LiteLLM, or custom | Your choice |

When you run it, the agent:
1. Listens for your voice input
2. Transcribes it to text
3. Sends it to the LLM backend for an answer
4. Speaks the answer aloud

---

## Configuration

Edit `voice_agent/config.py` to set your preferences:

```python
# LLM backend options:
#   "ollama"       → Ollama (free, local, recommended)
#   "openai"       → OpenAI API (requires OPENAI_API_KEY env var)
#   "litellm"      → LiteLLM (routes to many providers)
#   "custom"       → Your own API endpoint
#   "mock"         → Returns canned responses (testing only)

LLM_BACKEND = "ollama"
LLM_MODEL  = "llama3.2"       # model name for your backend
TTS_ENGINE = "edge-tts"       # "edge-tts" or "pyttsx3" (offline fallback)
STT_ENGINE = "whisper"        # "whisper" or "speech_recognition"
VOICE       = "en-US-JennyNeural"  # edge-tts voice name
```

### Environment Variables

```bash
# For OpenAI backend
export OPENAI_API_KEY="sk-..."

# For LiteLLM backend  
export OPENAI_API_KEY="sk-..."   # or whatever your provider needs

# For Ollama (make sure Ollama is running locally)
# No env vars needed — just have Ollama installed and running
```

---

## LLM Backend Options

### Ollama (Recommended — Free, Local)

Install Ollama: https://ollama.ai

```bash
ollama pull llama3.2   # or mistral, llama3.1, etc.
```

Set `LLM_BACKEND = "ollama"` in config.

### OpenAI

```bash
export OPENAI_API_KEY="sk-..."
```

Set `LLM_BACKEND = "openai"`.

### LiteLLM

Routes to 100+ providers through one API.

```bash
export OPENAI_API_KEY="sk-..."   # your provider key
```

Set `LLM_BACKEND = "litellm"`.

### Custom API

Set `LLM_BACKEND = "custom"` and implement `voice_agent/llm.py`'s `CustomLLM` class.

---

## Requirements

| Tool | Why |
|---|---|
| Python 3.9+ | Runtime |
| edge-tts | Free, high-quality TTS (no API key) |
| openai | OpenAI API + LiteLLM support |
| ollama | Local LLM runtime (if using Ollama) |
| SpeechRecognition | STT fallback |
| pyaudio | Microphone input (for SpeechRecognition) |
| pyttsx3 | Offline TTS fallback (no internet needed) |
| whisper | Offline STT (optional, heavier) |

> **Windows audio note:** `pyaudio` needs `pip install pipwin && pipwin install pyaudio` on Windows if the normal install fails.

---

## Project Structure

```
voice_agent/
├── __init__.py      # Package init
├── cli.py           # Entry point — parses args, starts the agent
├── agent.py         # Main loop: listen → transcribe → answer → speak
├── stt.py           # Speech recognition (Whisper / SpeechRecognition)
├── tts.py           # Text-to-speech (edge-tts / pyttsx3)
├── llm.py           # LLM backends (Ollama / OpenAI / LiteLLM / custom)
└── config.py        # All user-configurable settings
```

---

## CLI Usage

```bash
# Start the voice agent
python -m voice_agent

# With options
python -m voice_agent --backend ollama --model llama3.2 --voice en-US-AriaNeural
```

### CLI Options

| Flag | Default | Description |
|---|---|---|
| `--backend` | from config | LLM backend: ollama, openai, litellm |
| `--model` | from config | Model name |
| `--voice` | from config | TTS voice name (edge-tts voices) |
| `--verbose` | False | Print transcriptions and responses to console |

---

## edge-tts Voices

List available voices:

```bash
edge-tts --list-voices
```

Popular ones:
- `en-US-JennyNeural` — English, natural
- `en-US-AriaNeural` — English, warm
- `en-GB-SoniaNeural` — British English
- `es-ES-MariaNeural` — Spanish
- `fr-FR-DeniseNeural` — French

---

## Troubleshooting

### "No module named 'voice_agent'"
Make sure you're in the project root and the venv is activated.

### "pyaudio installation failed" (Windows)
```bash
pip install pipwin
pipwin install pyaudio
```

### "Whisper not available"
Whisper needs `pip install openai-whisper` which pulls in PyTorch. If you don't need offline STT, set `STT_ENGINE = "speech_recognition"` in config instead.

### "edge-tts fails with network error"
edge-tts needs internet access (contacts Microsoft's Edge servers). If you're offline, set `TTS_ENGINE = "pyttsx3"` in config for a fully offline fallback.

### "Ollama not found"
Make sure Ollama is installed and running:
```bash
ollama serve   # in one terminal
```

---

## License

MIT
