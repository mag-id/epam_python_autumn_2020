"""
Unit tests for `calculator` module.
"""

import pytest

from homework_1.sample_project.calculator.calc import check_power_of_2


@pytest.mark.parametrize(
    ["value", "expected_result"],
    [
        (-2, False),
        (-1, False),
        (-0, False),
        (0, False),
        (1, True),
        (2, True),
        (12, False),
        (65536, True),
    ],
)
def test_power_of_2(value: int, expected_result: bool):
    """Pass test if result of `value` is equal to `expected_result`."""
    actual_result = check_power_of_2(value)

    assert actual_result == expected_result
