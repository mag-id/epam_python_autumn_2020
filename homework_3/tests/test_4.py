"""
Unit tests for module `homework_3.tasks.task_4`.
"""
import pytest

from homework_3.tasks.task_4 import is_armstrong


@pytest.mark.parametrize(
    ["number", "expected_result"],
    [
        pytest.param(0, True, id="True: 0 is armstrong  (0^1 == 0)."),
        pytest.param(1, True, id="True: 1 is armstrong (1^1 == 1)."),
        pytest.param(9, True, id="True: 9 is armstrong (9^1 == 9)."),
        pytest.param(153, True, id="True: 153 is armstrong (1^3 + 5^3 + 3^3 == 153)."),
    ],
)
def test_true_is_armstrong(number: int, expected_result: bool):
    """Passes test if `is_armstrong(number)` is equal to `expected_result`."""
    assert is_armstrong(number) == expected_result


@pytest.mark.parametrize(
    ["number", "expected_result"],
    [
        pytest.param(10, False, id="False: 10 is not armstrong (1^2 + 0^2 != 10)."),
        pytest.param(13, False, id="False: 13 is not armstrong (1^2 + 3^2 != 13)."),
        pytest.param(
            144, False, id="False: 13 is not armstrong (1^3 + 4^3 + 4^3 != 144)."
        ),
    ],
)
def test_fasle_is_armstrongs(number: int, expected_result: bool):
    """Passes test if `is_armstrong(number)` is equal to `expected_result`."""
    assert is_armstrong(number) == expected_result
