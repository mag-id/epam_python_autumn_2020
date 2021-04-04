"""
Unit tests for module `homework_2.tasks.task_2`.
"""
from typing import List, Tuple

import pytest

from homework_2.tasks.task_2 import (
    ARRAY_LENGTH_MESSAGE,
    LEAST_ELEMENT_MESSAGE,
    MOST_ELEMENT_MESSAGE,
    major_and_minor_elem,
)


@pytest.mark.parametrize(
    ["array", "expected_result"],
    [
        pytest.param(
            [3, 2, 3],
            (3, 2),
            id="3 is the most and 2 is the least common in [3, 2, 3].",
        ),
        pytest.param(
            [2, 2, 1, 1, 1, 2, 2],
            (2, 1),
            id="2 is the most and 1 is the least common in [2, 2, 1, 1, 1, 2, 2].",
        ),
    ],
)
def test_common_cases_for_major_and_minor_elem(
    array: List[int], expected_result: Tuple[int, int]
):
    """
    Passes test if `major_and_minor_elem`(`array`)
    is equal to `expected_result`.
    """
    assert major_and_minor_elem(array) == expected_result


@pytest.mark.parametrize(
    ["array", "expected_exception", "expected_message"],
    [
        pytest.param(
            [0, 0],
            ValueError,
            ARRAY_LENGTH_MESSAGE,
            id="len([0, 0]) < 3",
        ),
        pytest.param(
            [1, 1, 0, 0],
            ValueError,
            MOST_ELEMENT_MESSAGE,
            id="The most common element in [1, 1, 0, 0] can not be defined.",
        ),
        pytest.param(
            [0, 0, 0],
            ValueError,
            LEAST_ELEMENT_MESSAGE,
            id="The least common element in [0, 0, 0] can not be defined.",
        ),
        pytest.param(
            [1, 1, 1, 2, 3],
            ValueError,
            LEAST_ELEMENT_MESSAGE,
            id="The least common element in [1, 1, 1, 2, 3] can not be defined.",
        ),
    ],
)
def test_value_error_cases_for_major_and_minor_elem(
    array: List[int], expected_exception: Exception, expected_message: str
):
    """
    Passes test if `major_and_minor_elem`(`array`)
    raises `expected_exception` with `expected_message`.
    """
    with pytest.raises(expected_exception) as exception_info:
        major_and_minor_elem(array)
    assert str(exception_info.value) == expected_message
