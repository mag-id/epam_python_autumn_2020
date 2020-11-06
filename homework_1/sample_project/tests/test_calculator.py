"""
Unit tests for `calculator` module.
"""

import pytest

from homework_1.sample_project.calculator.calc import check_power_of_2


@pytest.mark.parametrize(
    ["value", "expected_result"],
    [
        pytest.param(
            -1,
            False,
            id="False case: -1 is not a power of 2.",
        ),
        pytest.param(
            0,
            False,
            id="False case: 0 is not a power of 2.",
        ),
        pytest.param(
            1,
            True,
            id="True case: 2**0 = 1.",
        ),
        pytest.param(
            2,
            True,
            id="True case: 2**1 = 2.",
        ),
        pytest.param(
            12,
            False,
            id="False case: 12 is not a power of 2.",
        ),
        pytest.param(
            65536,
            True,
            id="True case: 2**16 = 65536.",
        ),
        pytest.param(
            2 ** 29,
            True,
            id="True case: 2**29.",
        ),
        pytest.param(
            2 ** (49 - 1),
            True,
            id="True case: 2**(49-1).",
        ),
        pytest.param(
            2 ** (53 + 1),
            True,
            id="True case: 2**(53+1).",
        ),
    ],
)
def test_power_of_2(value: int, expected_result: bool):
    """
    Passes test if `check_power_of_2`(`value`)
    is equal to `expected_result`.
    """
    assert check_power_of_2(value) == expected_result
