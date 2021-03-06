from typing import Tuple, Union

import pytest
from cx_core.stepper import Stepper


class FakeStepper(Stepper):
    def step(self, value: float, direction: str) -> Tuple[Union[int, float], bool]:
        return 0, True


@pytest.mark.parametrize(
    "direction_input, previous_direction, expected_direction",
    [
        (Stepper.UP, Stepper.UP, Stepper.UP),
        (Stepper.DOWN, Stepper.DOWN, Stepper.DOWN),
        (Stepper.UP, Stepper.DOWN, Stepper.UP),
        (Stepper.DOWN, Stepper.UP, Stepper.DOWN),
        (Stepper.TOGGLE, Stepper.TOGGLE_UP, Stepper.TOGGLE_DOWN),
        (Stepper.TOGGLE, Stepper.TOGGLE_DOWN, Stepper.TOGGLE_UP),
    ],
)
def test_get_direction(
    direction_input: str, previous_direction: str, expected_direction: str
):
    stepper = FakeStepper()
    stepper.previous_direction = previous_direction

    direction_output = stepper.get_direction(0, direction_input)

    assert direction_output == expected_direction


@pytest.mark.parametrize(
    "direction_input, expected_sign",
    [
        (Stepper.UP, 1),
        (Stepper.DOWN, -1),
        (Stepper.TOGGLE_UP, 1),
        (Stepper.TOGGLE_DOWN, -1),
    ],
)
def test_sign(direction_input: str, expected_sign: int):
    stepper = FakeStepper()
    sign_output = stepper.sign(direction_input)
    assert sign_output == expected_sign
