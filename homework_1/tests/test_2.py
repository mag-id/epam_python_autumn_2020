"""
Unit tests for module `homework_1.tasks.task_2`.
"""

from typing import Sequence

import pytest

from homework_1.tasks.task_2 import check_fibonacci


@pytest.mark.parametrize(
    ["data", "expected_result"],
    [
        pytest.param(
            [0],
            True,
            id="Boundary case: 0 is the Fibonacci seed.",
        ),
        pytest.param(
            [0, 1],
            True,
            id="Boundary case: [0, 1] is the Fibonacci seeds.",
        ),
        pytest.param(
            [0, 0, 0],
            False,
            id="False case: [0, 0, 0].",
        ),
        pytest.param(
            [0, 1, 1],
            True,
            id="True case: [0, 1, 1].",
        ),
        pytest.param(
            [1, 0, 1],
            False,
            id="False case: [1, 0, 1].",
        ),
        pytest.param(
            [1, 1, 3],
            False,
            id="False case: [1, 1, 3] must starts from 0.",
        ),
        pytest.param(
            [0, 1, 1, 3, 2, 5, 8, 13, 21],
            False,
            id="False case: [0, 1, 1, 3, 2 ... 21] - Fibonacci invariant is broken.",
        ),
        pytest.param(
            [0, 1, 1, 2, 3, 5, 8, 13, 21],
            True,
            id="True case: [0, ... 21] is the Fibonacci sequence.",
        ),
        pytest.param(
            (0, 1, 1, 2, 3, 5, 8, 13, 21),
            True,
            id="True case: (0, ... 21) is the Fibonacci sequence.",
        ),
    ],
)
def test_check_fibonacci(data: Sequence[int], expected_result: bool):
    """
    Passes test if `check_fibonacci`(`data`)
    is equal to `expected_result`.
    """
    assert check_fibonacci(data) == expected_result
