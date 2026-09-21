# Personal Chat-Style AI Chatbot

A local Flask application that creates an **AI simulation of communication style** from an imported text chat. It does not impersonate a person, assert their identity, or infer psychological traits.

## Features

- Tolerant WhatsApp-like text parsing, multiline messages, emoji, and participant detection.
- Target selection and structured, observable style analysis.
- SQLite storage with historical messages separate from current session memory.
- Compact retrieval of relevant historical exchanges (with a dependency-free similarity fallback).
- Provider abstraction with a mock provider for offline development and OpenAI-compatible HTTP providers.
- Dark, responsive chat UI, import preview, settings, deletion controls, and tests.

## Install and run

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # Windows: copy .env.example .env
python app.py
```

Open http://127.0.0.1:5000/import, upload a `.txt` export, preview it, select the target, and start chatting. The default `mock` provider works without an API key. Configure an OpenAI-compatible provider with `LLM_PROVIDER=openai`, `LLM_API_KEY`, `LLM_MODEL`, and optionally `LLM_BASE_URL`.

## Architecture

`parser_service` parses raw text; `personality_service` calculates cached pattern statistics; `retrieval_service` selects a small set of relevant exchanges; `prompt_service` builds the disclosure-aware prompt; `llm_service` isolates provider calls. Historical data and current session messages are separate SQLite tables.

The included retriever is a lightweight cosine similarity implementation so the project runs without a large model download. A sentence-transformers/FAISS adapter can be added behind `retrieval_service` for larger datasets without changing routes or prompts. Embeddings should be cached when added.

## Privacy and safety

Imported chat data is stored locally in `data/chatbot.sqlite3` and is never logged in full. Do not commit `.env` or real conversations. When an external provider is configured, only the compact style profile, retrieved examples, and recent conversation context are sent to that provider; that data leaves your machine. Use Settings to delete imported and session data. The application uses style patterns only and avoids unsupported biographical or psychological claims.

## Troubleshooting and extension

- “No supported messages”: use lines like `12/08/2026, 21:32 - Alex: hello`; add a parser adapter for another export format.
- LLM errors: check provider, model, key, and base URL in `.env`; restart Flask after changes.
- For another provider, implement `LLMProvider.generate` in `app/services/llm_service.py` and select it in `get_provider`.
- Run tests with `pytest`.
