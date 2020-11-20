"""
Unit tests for module `homework_3.tasks.task_4`.
"""
import pytest

from homework_3.tasks.task_4 import is_armstrong


@pytest.mark.parametrize(
    [
        "number",
    ],
    [
        pytest.param(0, id="True: 0 is armstrong  (0^1 == 0)."),
        pytest.param(1, id="True: 1 is armstrong (1^1 == 1)."),
        pytest.param(9, id="True: 9 is armstrong (9^1 == 9)."),
        pytest.param(153, id="True: 153 is armstrong (1^3 + 5^3 + 3^3 == 153)."),
    ],
)
def test_true_is_armstrong(number: int):
    """Passes test if `is_armstrong(number)` is `True`."""
    assert is_armstrong(number)


@pytest.mark.parametrize(
    [
        "number",
    ],
    [
        pytest.param(10, id="False: 10 is not armstrong (1^2 + 0^2 != 10)."),
        pytest.param(13, id="False: 13 is not armstrong (1^2 + 3^2 != 13)."),
        pytest.param(144, id="False: 13 is not armstrong (1^3 + 4^3 + 4^3 != 144)."),
    ],
)
def test_fasle_is_armstrongs(number: int):
    """Passes test if `is_armstrong(number)` is `False`."""
    assert is_armstrong(number) is False
