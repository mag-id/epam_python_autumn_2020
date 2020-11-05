"""
Unit tests for module `homework_1.tasks.task_5`.
"""

from typing import List

import pytest

from homework_1.tasks.task_5 import find_maximal_subarray_sum


@pytest.mark.parametrize(
    ["array", "max_subarray_length", "expected_result"],
    [
        pytest.param(
            [],
            0,
            "IndexError",
            id="False case: array=[] and max_subarray_length=0 raises IndexError.",
        ),
        pytest.param(
            [1],
            0,
            "ValueError",
            id="False case: array=[1] and max_subarray_length=0 raises ValueError.",
        ),
        pytest.param(
            [],
            3,
            "IndexError",
            id="False case: array=[] and max_subarray_length=3 raises IndexError.",
        ),
        pytest.param(
            [1],
            1,
            1,
            id="True case: array=[1], max_subarray_length=1 returns 1.",
        ),
        pytest.param(
            [-1],
            1,
            -1,
            id="True case: array=[-1], max_subarray_length=1 returns -1.",
        ),
        pytest.param(
            [1],
            3,
            1,
            id="True case: array=[1], max_subarray_length=3 returns 1.",
        ),
        pytest.param(
            [1, -3],
            3,
            1,
            id="True case: array=[1, -3], max_subarray_length=3 returns 1.",
        ),
        pytest.param(
            [1, 3],
            3,
            4,
            id="True case: array=[1, 3], max_subarray_length=3 returns 4.",
        ),
        pytest.param(
            [1, 3, -1, -3, 5, 3, 6, 7],
            1,
            7,
            id="True case: array=[1, 3, -1, -3, 5, 3, 6, 7], max_subarray_length=1 returns 7.",
        ),
        pytest.param(
            [1, 3, -1, -3, 5, 3, 6, 7],
            3,
            16,
            id="True case: array=[1, 3, -1, -3, 5, 3, 6, 7], max_subarray_length=3 returns 16.",
        ),
        pytest.param(
            [1, 3, -1, -3, 10, 3, 6, 7],
            3,
            19,
            id="True case: array=[1, 3, -1, -3, 10, 3, 6, 7], max_subarray_length=3 returns 19.",
        ),
        pytest.param(
            [1, 3, -1, -3, 50, -3, 6, 7],
            10,
            60,
            id="True case: array=[1, 3, -1, -3, 50, -3, 6, 7], max_subarray_length=10 returns 60.",
        ),
    ],
)
def test_find_maximal_subarray_sum(
    array: List[int], max_subarray_length: int, expected_result: int
):
    """
    Passes test if `find_maximal_subarray_sum`(`array`, `max_subarray_length`)
    is equal to `expected_result`.
    """
    actual_result = None
    try:
        actual_result = find_maximal_subarray_sum(array, max_subarray_length)
    except IndexError:
        actual_result = "IndexError"
    except ValueError:
        actual_result = "ValueError"
    finally:
        assert actual_result == expected_result
