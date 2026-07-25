from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any


@dataclass
class Skill:
    name: str
    description: str
    parameters: dict[str, Any]
    handler: Callable[..., str]


class SkillRegistry:
    def __init__(self) -> None:
        self._skills: dict[str, Skill] = {}

    def register(self, skill: Skill) -> None:
        self._skills[skill.name] = skill

    def get(self, name: str) -> Skill | None:
        return self._skills.get(name)

    def all(self) -> list[Skill]:
        return list(self._skills.values())

    def as_tool_specs(self) -> list[dict[str, Any]]:
        return [
            {"name": s.name, "description": s.description, "input_schema": s.parameters}
            for s in self._skills.values()
        ]


registry = SkillRegistry()


def skill(
    name: str, description: str, parameters: dict[str, Any]
) -> Callable[[Callable[..., str]], Callable[..., str]]:
    """Register a function as a skill Claude can invoke as a tool."""

    def decorator(func: Callable[..., str]) -> Callable[..., str]:
        registry.register(Skill(name=name, description=description, parameters=parameters, handler=func))
        return func

    return decorator
