from typing import Any, Dict

import pytest
from cx_core.controller import Controller
from cx_core.integration.z2m import Z2MIntegration
from pytest_mock import MockerFixture


@pytest.mark.parametrize(
    "data, action_key, handle_action_called, expected_called_with",
    [
        ({"payload": '{"event_1": "action_1"}'}, "event_1", True, "action_1"),
        ({}, None, False, Any),
        ({"payload": '{"action": "action_1"}'}, None, True, "action_1"),
        ({"payload": '{"event_1": "action_1"}'}, "event_2", False, "Any"),
        ({"payload": '{"action_rate": 195}'}, "action", False, "Any"),
    ],
)
@pytest.mark.asyncio
async def test_event_callback(
    fake_controller: Controller,
    mocker: MockerFixture,
    data: Dict,
    action_key: str,
    handle_action_called: bool,
    expected_called_with: str,
):
    handle_action_patch = mocker.patch.object(fake_controller, "handle_action")
    z2m_integration = Z2MIntegration(fake_controller, {})
    z2m_integration.kwargs = (
        {"action_key": action_key} if action_key is not None else {}
    )
    await z2m_integration.event_callback("test", data, {})

    if handle_action_called:
        handle_action_patch.assert_called_once_with(expected_called_with)
    else:
        handle_action_patch.assert_not_called()
