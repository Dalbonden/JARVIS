from jarvis.skills import base, example_skill  # noqa: F401


def test_get_current_time_is_registered():
    matched = base.registry.get("get_current_time")
    assert matched is not None
    assert matched.handler()


def test_tool_specs_include_registered_skills():
    names = {spec["name"] for spec in base.registry.as_tool_specs()}
    assert "get_current_time" in names
