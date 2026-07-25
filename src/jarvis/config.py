from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_prefix="JARVIS_", extra="ignore")

    anthropic_api_key: str = ""
    model: str = "claude-sonnet-5"
    system_prompt: str = (
        "You are JARVIS, a helpful personal AI assistant. Be concise and use the "
        "available tools when they let you answer more accurately."
    )
