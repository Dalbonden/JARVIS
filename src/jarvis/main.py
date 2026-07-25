from __future__ import annotations

from jarvis.audio.stt import ConsoleSpeechToText
from jarvis.audio.tts import ConsoleTextToSpeech
from jarvis.brain.assistant import Assistant
from jarvis.config import Settings


def run() -> None:
    settings = Settings()
    assistant = Assistant(settings)
    stt = ConsoleSpeechToText()
    tts = ConsoleTextToSpeech()

    print("JARVIS is online. Type 'exit' to quit.")
    while True:
        try:
            user_input = stt.listen().strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if user_input.lower() in {"exit", "quit"}:
            break
        if not user_input:
            continue
        tts.speak(assistant.ask(user_input))


if __name__ == "__main__":
    run()
