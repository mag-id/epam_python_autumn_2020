"""
Unit tests for module `homework_2.tasks.task_5`.
"""
import string

import pytest

from homework_2.tasks.task_5 import custom_range


@pytest.mark.parametrize(
    ["unique_values", "args", "expected_result"],
    [
        pytest.param(
            string.ascii_lowercase,
            ("g",),
            ["a", "b", "c", "d", "e", "f"],
            id="Common case: iterable is ascii_lowercase, start is 'g'.",
        ),
        pytest.param(
            string.ascii_lowercase,
            ("g", "p"),
            ["g", "h", "i", "j", "k", "l", "m", "n", "o"],
            id="Common case: iterable is ascii_lowercase, start is 'g', end is 'p'.",
        ),
        pytest.param(
            string.ascii_lowercase,
            ("g", "p", -2),
            ["p", "n", "l", "j", "h"],
            id="Common case: iterable is ascii_lowercase, start 'g', end 'p', step -2.",
        ),
    ],
)
def test_common_case_custom_range(unique_values, args, expected_result):
    """
    Passes test if `common_case_custom_range`(`unique_valuess`, `args`)
    is equal to `expected_result`.
    """
    assert custom_range(unique_values, *args) == expected_result


@pytest.mark.parametrize(
    ["unique_values", "arg", "step", "expected_result"],
    [
        pytest.param(
            string.ascii_lowercase,
            "g",
            -1,
            ["g", "f", "e", "d", "c", "b"],
            id="Common case: iterable is ascii_lowercase, start is 'g', step is -1.",
        ),
        pytest.param(
            string.ascii_lowercase,
            "g",
            2,
            ["a", "c", "e"],
            id="Common case: iterable is ascii_lowercase, start is 'g', step is 2.",
        ),
    ],
)
def test_step_for_custom_range(unique_values, arg, step, expected_result):
    """
    Passes test if `common_case_custom_range`(`unique_valuess`, `arg`, `step=step`)
    is equal to `expected_result`.
    """
    assert custom_range(unique_values, arg, step=step) == expected_result
