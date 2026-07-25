from __future__ import annotations

from datetime import UTC, datetime

from jarvis.skills.base import skill


@skill(
    name="get_current_time",
    description="Get the current date and time (UTC).",
    parameters={"type": "object", "properties": {}, "required": []},
)
def get_current_time() -> str:
    return datetime.now(UTC).isoformat()
