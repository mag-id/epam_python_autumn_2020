"""
Unit tests for module `homework_1.tasks.task_4`.
"""

from typing import List

import pytest

from homework_1.tasks.task_4 import check_sum_of_four


@pytest.mark.parametrize(
    ["four_values", "expected_result"],
    [
        pytest.param(
            [[], [], [], []],
            0,
            id="Number of zero-sum tuples from [[], [], [], []] is 0.",
        ),
        pytest.param(
            [[1], [1], [1], [1]],
            0,
            id="Number of zero-sum tuples from [[1], [1], [1], [1]] is 0.",
        ),
        pytest.param(
            [[0], [0], [0], [0]],
            1,
            id="Number of zero-sum tuples from [[0], [0], [0], [0]] is 1.",
        ),
        pytest.param(
            [[1, 1], [0, 0], [0, 0], [0, 0]],
            0,
            id="Number of zero-sum tuples from [[1, 1], [0, 0], [0, 0], [0, 0]] is 0.",
        ),
        pytest.param(
            [[1, -1], [0, 0], [0, 0], [0, 0]],
            0,
            id="Number of zero-sum tuples from [[1, -1], [0, 0], [0, 0], [0, 0]] is 0.",
        ),
        pytest.param(
            [[1, 0], [-1, 0], [0, 0], [0, 0]],
            8,
            id="Number of zero-sum tuples from [[1, 0], [-1, 0], [0, 0], [0, 0]] is 8.",
        ),
        pytest.param(
            [[1, 0], [0, -1], [0, 0], [0, 0]],
            8,
            id="Number of zero-sum tuples from [[1, 0], [0, -1], [0, 0], [0, 0]] is 8.",
        ),
        pytest.param(
            [[1, 0], [0, 0], [0, 0], [0, 0]],
            8,
            id="Number of zero-sum tuples from [[1, 0], [0, 0], [0, 0], [0, 0]] is 8.",
        ),
        pytest.param(
            [[0, 0], [0, 0], [0, 0], [0, 0]],
            16,
            id="Number of zero-sum tuples from [[0, 0], [0, 0], [0, 0], [0, 0]] is 16.",
        ),
    ],
)
def test_check_sum_of_four(four_values: List[List[int]], expected_result: int):
    """
    Passes test if `check_sum_of_four`(`*four_values`) is equal to `expected_result`.
    """
    a_values, b_values, c_values, d_values = four_values

    actual_result = check_sum_of_four(a_values, b_values, c_values, d_values)

    assert actual_result == expected_result
