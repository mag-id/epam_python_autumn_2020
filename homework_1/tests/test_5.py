"""
Unit tests for module `homework_1.tasks.task_5`.
"""

from typing import List

import pytest

from homework_1.tasks.task_5 import (
    INDEX_ERROR_TEXT,
    VALUE_ERROR_TEXT,
    find_maximal_subarray_sum,
)


@pytest.mark.parametrize(
    ["array", "max_subarray_length", "expected_exception", "expected_message"],
    [
        pytest.param(
            [],
            0,
            IndexError,
            INDEX_ERROR_TEXT,
            id="array=[] and max_subarray_length=0 raises IndexError.",
        ),
        pytest.param(
            [1],
            0,
            ValueError,
            VALUE_ERROR_TEXT,
            id="array=[1] and max_subarray_length=0 raises ValueError.",
        ),
        pytest.param(
            [],
            3,
            IndexError,
            INDEX_ERROR_TEXT,
            id="array=[] and max_subarray_length=3 raises IndexError.",
        ),
    ],
)
def test_exceptions_in_find_maximal_subarray_sum(
    array: List[int],
    max_subarray_length: int,
    expected_exception: Exception,
    expected_message: str,
):
    """
    Passes test if `find_maximal_subarray_sum`(`array`, `max_subarray_length`)
    raises `expected_exception` with `expected_message`.
    """
    with pytest.raises(expected_exception) as exception_info:
        find_maximal_subarray_sum(array, max_subarray_length)
    assert str(exception_info.value) == expected_message


@pytest.mark.parametrize(
    ["array", "max_subarray_length", "expected_result"],
    [
        pytest.param(
            [1],
            1,
            1,
            id="array=[1], max_subarray_length=1 returns 1",
        ),
        pytest.param(
            [-1],
            1,
            -1,
            id="array=[-1], max_subarray_length=1 returns -1",
        ),
        pytest.param(
            [1],
            3,
            1,
            id="array=[1], max_subarray_length=3 returns 1",
        ),
        pytest.param(
            [1, -3],
            3,
            1,
            id="array=[1, -3], max_subarray_length=3 returns 1",
        ),
        pytest.param(
            [1, 3],
            3,
            4,
            id="array=[1, 3], max_subarray_length=3 returns 4",
        ),
        pytest.param(
            [1, 3, -1, -3, 5, 3, 6, 7],
            1,
            7,
            id="array=[1, 3, -1, -3, 5, 3, 6, 7], max_subarray_length=1 returns 7",
        ),
        pytest.param(
            [1, 3, -1, -3, 5, 3, 6, 7],
            3,
            16,
            id="array=[1, 3, -1, -3, 5, 3, 6, 7], max_subarray_length=3 returns 16",
        ),
        pytest.param(
            [1, 3, -1, -3, 10, 3, 6, 7],
            3,
            19,
            id="array=[1, 3, -1, -3, 10, 3, 6, 7], max_subarray_length=3 returns 19",
        ),
        pytest.param(
            [1, 3, -1, -3, 50, -3, 6, 7],
            10,
            60,
            id="array=[1, 3, -1, -3, 50, -3, 6, 7], max_subarray_length=10 returns 60",
        ),
        pytest.param(
            [-2, 1, -3, 4, -1, 2, 1, -5, 4],
            3,
            5,
            id="array=[-2, 1, -3, 4, -1, 2, 1, -5, 4], max_subarray_length=3 returns 5",
        ),
        pytest.param(
            [-3, -4, -3, -1, -1, -3, -4],
            3,
            -1,
            id="array=[-3, -4, -3, -1, -1, -3, -4], max_subarray_length=3 returns -1",
        ),
    ],
)
def test_true_find_maximal_subarray_sum(
    array: List[int], max_subarray_length: int, expected_result: int
):
    """
    Passes test if `find_maximal_subarray_sum`(`array`, `max_subarray_length`)
    is equal to `expected_result`.
    """
    assert find_maximal_subarray_sum(array, max_subarray_length) == expected_result
