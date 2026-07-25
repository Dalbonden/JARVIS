from __future__ import annotations

from typing import Any

from anthropic import Anthropic

from jarvis.config import Settings
from jarvis.skills import base as skills
from jarvis.skills import example_skill  # noqa: F401  registers the built-in skills


class Assistant:
    """Wraps the Claude API in a conversation loop that can call registered skills."""

    def __init__(self, settings: Settings, client: Any | None = None) -> None:
        self.settings = settings
        self.client = client or Anthropic(api_key=settings.anthropic_api_key)
        self.history: list[dict[str, Any]] = []

    def ask(self, user_message: str) -> str:
        self.history.append({"role": "user", "content": user_message})
        tools = skills.registry.as_tool_specs()

        while True:
            response = self.client.messages.create(
                model=self.settings.model,
                max_tokens=1024,
                system=self.settings.system_prompt,
                messages=self.history,
                tools=tools,
            )
            self.history.append({"role": "assistant", "content": response.content})

            if response.stop_reason != "tool_use":
                return "".join(block.text for block in response.content if block.type == "text")

            tool_results = []
            for block in response.content:
                if block.type != "tool_use":
                    continue
                matched_skill = skills.registry.get(block.name)
                result = (
                    matched_skill.handler(**block.input)
                    if matched_skill is not None
                    else f"Unknown skill: {block.name}"
                )
                tool_results.append(
                    {"type": "tool_result", "tool_use_id": block.id, "content": result}
                )
            self.history.append({"role": "user", "content": tool_results})
