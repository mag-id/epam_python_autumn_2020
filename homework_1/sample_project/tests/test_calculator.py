"""
Unit tests for `calculator` module.
"""

import pytest

from homework_1.sample_project.calculator.calc import check_power_of_2


@pytest.mark.parametrize(
    ["value", "expected_result"],
    [
        pytest.param(-65536, False, id="Negative case: -65536 is not a power of 2."),
        pytest.param(-12, False, id="Negative case: -12 is not a power of 2."),
        pytest.param(-2, False, id="Negative case: -2 is not a power of 2."),
        pytest.param(-1, False, id="Negative case: -1 is not a power of 2."),
        pytest.param(0, False, id="Boundary case: 0 is not a power of 2."),
        pytest.param(1, True, id="Boundary case: 2**0 = 1."),
        pytest.param(2, True, id="Simple case: 2**1 = 2."),
        pytest.param(12, False, id="Simple case: 12 is not a power of 2."),
        pytest.param(65536, True, id="Simple case: 2**16 = 65536."),
    ],
)
def test_power_of_2(value: int, expected_result: bool):
    """
    Passes test if `check_power_of_2`(`value`)
    is equal to `expected_result`.
    """
    actual_result = check_power_of_2(value)

    assert actual_result == expected_result
