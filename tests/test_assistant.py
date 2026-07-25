from types import SimpleNamespace

from jarvis.brain.assistant import Assistant
from jarvis.config import Settings


class FakeMessages:
    def __init__(self, responses):
        self._responses = iter(responses)

    def create(self, **kwargs):
        return next(self._responses)


class FakeClient:
    def __init__(self, responses):
        self.messages = FakeMessages(responses)


def make_text_response(text):
    return SimpleNamespace(content=[SimpleNamespace(type="text", text=text)], stop_reason="end_turn")


def make_tool_use_response(name, tool_input, tool_id="tool_1"):
    return SimpleNamespace(
        content=[SimpleNamespace(type="tool_use", name=name, input=tool_input, id=tool_id)],
        stop_reason="tool_use",
    )


def test_ask_returns_plain_text_response():
    settings = Settings(anthropic_api_key="test")
    client = FakeClient([make_text_response("Hello there")])
    assistant = Assistant(settings, client=client)

    assert assistant.ask("hi") == "Hello there"


def test_ask_executes_a_skill_before_returning_text():
    settings = Settings(anthropic_api_key="test")
    client = FakeClient(
        [
            make_tool_use_response("get_current_time", {}),
            make_text_response("It's now."),
        ]
    )
    assistant = Assistant(settings, client=client)

    assert assistant.ask("what time is it") == "It's now."
