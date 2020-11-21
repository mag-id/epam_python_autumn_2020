"""
Unit tests for module `homework_2.tasks.task_4`.
"""
from typing import Any, Callable, Tuple

import pytest

from homework_2.tasks.task_4 import cache


@pytest.mark.parametrize(
    ["function", "args"],
    [
        pytest.param(
            lambda a, b: (a ** b) ** 2,
            (100, 200),
            id="Common case: cache(lambda ... ) returns same result.",
        ),
        pytest.param(
            cache(function=lambda a, b: (a ** b) ** 2),
            (100, 200),
            id="Common case: cache(cache(lambda ... )) returns same result.",
        ),
        pytest.param(
            lambda a: list(range(a)),
            (10,),
            id="Common case: cache(lambda: range ... ) returns same result.",
        ),
    ],
)
def test_common_case_for_cache(function: Callable, args: Tuple[Any]):
    """
    Passes test if result of `cache(function)` under `args` is stable.
    """
    cached_function = cache(function)
    assert cached_function(*args) == cached_function(*args)


def test_arg_kwarg_and_late_binding_for_cache():
    """
    Passes test if result of `cache(function)`
    under `args` and `kwargs` is stable.
    """

    def function(variable: int, multiplicator: int = 2):
        return (variable * multiplicator) + const

    const = 1
    cached_function = cache(function)
    first_result = cached_function(1)

    const = 2
    second_result = cached_function(1)

    third_result = function(1)

    assert first_result == second_result != third_result


def test_kwargs_for_cache():
    """
    Passes test if result of
    `cached_func(kwarg_one=value_one, kwarg_two=value_two)`
    and
    `cached_func(kwarg_two=value_two, kwarg_one=value_one)`
    is same object.

    (Passes test if inner cache (or hash) of `cache` is stable).
    """

    def mult(first=1, second=1):
        return first * second

    cached_mult = cache(mult)
    first_result = cached_mult(first=100, second=200)
    second_result = cached_mult(second=200, first=100)
    assert first_result is second_result  # assert id(first_result) == id(second_result)
