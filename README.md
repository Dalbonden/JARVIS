# JARVIS

A personal AI voice assistant built on the Claude API, with a pluggable skill
(tool) system.

## Setup

```bash
pip install -e ".[dev]"
cp .env.example .env  # then fill in JARVIS_ANTHROPIC_API_KEY
```

## Usage

```bash
jarvis
```

This starts a console loop: type a message, JARVIS replies (calling any
skills it needs along the way). Type `exit` to quit.

## Development

```bash
pytest          # run tests
ruff check .    # lint
```

## Adding a skill

Skills are plain Python functions registered as Claude tools. See
`src/jarvis/skills/example_skill.py`:

```python
from jarvis.skills.base import skill

@skill(
    name="get_current_time",
    description="Get the current date and time.",
    parameters={"type": "object", "properties": {}, "required": []},
)
def get_current_time() -> str:
    ...
```

Import the module once (e.g. from `jarvis.brain.assistant`) so the
`@skill` decorator runs and registers it.
