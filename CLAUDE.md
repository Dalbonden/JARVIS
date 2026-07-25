# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

JARVIS is a personal AI voice assistant. The "brain" is the Claude API; user-facing
speech is abstracted behind swappable interfaces so a real STT/TTS backend can be
plugged in later without touching the conversation logic. Capabilities beyond plain
chat (checking the time, controlling devices, etc.) are added as "skills" — plain
Python functions exposed to Claude as tools.

## Commands

```bash
pip install -e ".[dev]"   # install package + dev deps (pytest, ruff) into current env
cp .env.example .env      # then set JARVIS_ANTHROPIC_API_KEY

jarvis                    # run the console assistant loop (installed console script)

pytest                    # run the full test suite
pytest tests/test_assistant.py::test_ask_returns_plain_text_response   # run a single test

ruff check .              # lint
```

There is no separate build step; `pyproject.toml` (hatchling) packages `src/jarvis`.
CI (`.github/workflows/ci.yml`) runs `ruff check .` then `pytest` on every push/PR —
keep both green before pushing.

## Architecture

```
src/jarvis/
  config.py          Settings (pydantic-settings), read from env vars prefixed
                      JARVIS_ (or a .env file): anthropic_api_key, model, system_prompt.
  brain/assistant.py  Assistant: owns the conversation loop against the Claude API.
  skills/             The tool system Claude can call into.
    base.py           Skill dataclass + SkillRegistry + @skill decorator.
    example_skill.py  Sample skill (get_current_time); pattern for adding more.
  audio/              SpeechToText / TextToSpeech abstract interfaces, with
                      console-based default implementations (stt.py, tts.py).
  main.py             CLI entrypoint wiring STT -> Assistant -> TTS in a loop.
```

**Skill registration is import-order dependent.** `@skill(...)` registers a function
into the module-level `jarvis.skills.base.registry` at import time — a skill module
that is never imported never registers. `brain/assistant.py` imports
`jarvis.skills.example_skill` for exactly this reason (see the `noqa: F401` there).
When adding a new skill module, import it the same way (from `assistant.py`, or from
a new `skills/__init__.py` aggregator if the list grows) or it silently won't be
available to Claude.

**Assistant.ask() runs a full tool-use loop, not a single request/response.** It
appends the user turn, calls `messages.create` with `tools=registry.as_tool_specs()`,
and — as long as `stop_reason == "tool_use"` — dispatches each `tool_use` block to the
matching skill's `handler(**block.input)`, appends the `tool_result`s as a new user
turn, and calls the API again. Conversation state lives in `self.history`, a list of
raw Claude message dicts; there is no separate conversation/session abstraction. Any
change to message shape (e.g. adding image content) has to stay compatible with this
loop's assumption that assistant turns are `response.content` verbatim.

**Audio is stubbed intentionally.** `ConsoleSpeechToText`/`ConsoleTextToSpeech` just
wrap stdin/stdout so the assistant loop is testable and runnable without hardware or
extra dependencies. To add a real backend, implement `SpeechToText`/`TextToSpeech`
from `audio/stt.py` / `audio/tts.py` and swap the instantiation in `main.py` — don't
change the `Assistant` interface (`ask(str) -> str`) to accommodate a specific
backend.

**Tests fake the Anthropic client, not the network.** `tests/test_assistant.py`
passes a `FakeClient`/`FakeMessages` pair whose `.create()` returns canned
`SimpleNamespace` objects shaped like real Anthropic `Message` responses (`content`,
`stop_reason`). Follow this pattern for new tests that exercise the tool-use loop
rather than mocking HTTP.
