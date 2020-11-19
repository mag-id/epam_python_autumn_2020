"""
Unit tests for module `homework_4.tasks.task_4`.
"""
from typing import List

import pytest

from homework_4.tasks.task_4 import fizzbuzz


@pytest.mark.parametrize(
    ["counter", "expected_result"],
    [
        pytest.param(
            5,
            ["1", "2", "fizz", "4", "buzz"],
            id="3 is fizz, 5 is buzz.",
        ),
        pytest.param(
            15,
            [
                "1",
                "2",
                "fizz",
                "4",
                "buzz",
                "fizz",
                "7",
                "8",
                "fizz",
                "buzz",
                "11",
                "fizz",
                "13",
                "14",
                "fizzbuzz",
            ],
            id="3, 6, 9, 12 is fizz; 5, 10 is buzz; and 15 is fizzbuzz.",
        ),
    ],
)
def test_common_true_case_fizzbuzz(counter: int, expected_result: List[str]):
    """
    Passes test if result of `fizzbuzz(counter)` is equal to `expected_result`.
    """
    assert fizzbuzz(counter) == expected_result
