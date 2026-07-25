from __future__ import annotations

from abc import ABC, abstractmethod


class TextToSpeech(ABC):
    @abstractmethod
    def speak(self, text: str) -> None:
        """Render text as speech (or otherwise deliver it to the user)."""


class ConsoleTextToSpeech(TextToSpeech):
    """Prints text to stdout. Swap in a real backend (e.g. ElevenLabs) later."""

    def speak(self, text: str) -> None:
        print(f"jarvis> {text}")
