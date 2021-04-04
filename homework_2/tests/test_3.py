"""
Unit tests for module `homework_2.tasks.task_3`.
"""
from typing import List

import pytest

from homework_2.tasks.task_3 import combinations


@pytest.mark.parametrize(
    ["args", "expected_result"],
    [
        pytest.param(
            [
                [1],
            ],
            [
                [1],
            ],
            id="[1] gives 1 combinations: [[1]]",
        ),
        pytest.param(
            [
                [1],
                [2],
                [3],
            ],
            [
                [1, 2, 3],
            ],
            id="[1], [2], [3] gives 1 combinations: [[1, 2, 3]]",
        ),
        pytest.param(
            [
                [1, 2],
                [3, 4],
            ],
            [
                [1, 3],
                [1, 4],
                [2, 3],
                [2, 4],
            ],
            id="[1, 2], [3, 4] gives 4 combinations: [[1, 3], [1, 4], [2, 3], [2, 4]]",
        ),
        pytest.param(
            [
                [1, 2, 3],
                [4, 5, 6],
                [7, 8, 9],
            ],
            [
                [1, 4, 7],
                [1, 4, 8],
                [1, 4, 9],
                [1, 5, 7],
                [1, 5, 8],
                [1, 5, 9],
                [1, 6, 7],
                [1, 6, 8],
                [1, 6, 9],
                [2, 4, 7],
                [2, 4, 8],
                [2, 4, 9],
                [2, 5, 7],
                [2, 5, 8],
                [2, 5, 9],
                [2, 6, 7],
                [2, 6, 8],
                [2, 6, 9],
                [3, 4, 7],
                [3, 4, 8],
                [3, 4, 9],
                [3, 5, 7],
                [3, 5, 8],
                [3, 5, 9],
                [3, 6, 7],
                [3, 6, 8],
                [3, 6, 9],
            ],
            id="[1, 2, 3], [4, 5, 6], [7, 8, 9] gives 27 combinations.",
        ),
    ],
)
def test_common_cases_for_combinations(args: List[List], expected_result: List[List]):
    """
    Passes test if `combinations`(`args`)
    is equal to `expected_result`.
    """
    assert combinations(*args) == expected_result


@pytest.mark.parametrize(
    ["args", "expected_result"],
    [
        pytest.param(
            [[]],
            [],
            id="[] gives 1 combinations: [].",
        ),
        pytest.param(
            [
                [],
                [],
            ],
            [],
            id="[], [] gives 1 combinations: [].",
        ),
        pytest.param(
            [
                [],
                [1, 2, 3],
            ],
            [],
            id="[], [1, 2, 3] gives 1 combinations: [].",
        ),
        pytest.param(
            [
                [1, 2],
                [],
                [3],
            ],
            [],
            id="[1, 2], [], [3] gives 1 combinations: [].",
        ),
    ],
)
def test_empty_lists_for_combinations(args: List[List], expected_result: List[List]):
    """
    Passes test if `combinations`(`args`)
    is equal to `expected_result`.
    """
    assert combinations(*args) == expected_result


@pytest.mark.parametrize(
    ["args", "expected_result"],
    [
        pytest.param(
            [
                [1],
                [3, 4],
            ],
            [
                [1, 3],
                [1, 4],
            ],
            id="[1], [3, 4] gives 2 combinations: [[1, 3], [1, 4]].",
        ),
        pytest.param(
            [
                [1, 2],
                [3],
            ],
            [
                [1, 3],
                [2, 3],
            ],
            id="[1, 2], [3] gives 2 combinations: [[1, 3], [2, 3]].",
        ),
        pytest.param(
            [[1, 2], [3], [4, 5, 6]],
            [
                [1, 3, 4],
                [1, 3, 5],
                [1, 3, 6],
                [2, 3, 4],
                [2, 3, 5],
                [2, 3, 6],
            ],
            id="[1, 2], [3], [4, 5, 6] gives 6 combinations.",
        ),
    ],
)
def test_nonequal_lists_for_combinations(args: List[List], expected_result: List[List]):
    """
    Passes test if `combinations`(`args`)
    is equal to `expected_result`.
    """
    assert combinations(*args) == expected_result
