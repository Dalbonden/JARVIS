from __future__ import annotations

from abc import ABC, abstractmethod


class SpeechToText(ABC):
    @abstractmethod
    def listen(self) -> str:
        """Capture audio and return the transcribed text."""


class ConsoleSpeechToText(SpeechToText):
    """Reads text from stdin. Swap in a real backend (e.g. Whisper) later."""

    def listen(self) -> str:
        return input("you> ")
