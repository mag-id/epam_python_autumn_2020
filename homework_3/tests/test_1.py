"""
Unit tests for module `homework_3.tasks.task_1`.
"""
from typing import Any, Callable, Tuple

import pytest

from homework_3.tasks.task_1 import NON_VALID_TIMES, cache


@pytest.mark.parametrize(
    ["function", "args"],
    [
        pytest.param(
            lambda a, b: (a ** b) ** 2,
            (100, 200),
            id="Common case: @cache(times=1) returns same result.",
        ),
        pytest.param(
            lambda a: list(range(a)),
            (10,),
            id="Common case: @cache(times=1) returns same result.",
        ),
    ],
)
def test_common_case_for_cache(function: Callable, args: Tuple[Any]):
    """
    Passes test if result of `wrap(function)` under `args`
    decorated by `@cache(times=1)` is stable.
    """

    @cache(times=1)
    def wrap(func):
        return func

    cached_function = wrap(function)
    assert cached_function(*args) == cached_function(*args)


def test_times_for_cache():
    """
    Passes test if results of `call()` decorated by `@cache()` are stable.
    """

    @cache()
    def call():
        return counter

    counter = 0
    initial_call = call()

    counter = 1
    first_call = call()

    counter = 2
    second_call = call()

    counter = 3
    third_call = call()

    counter = 4
    fourth_call = call()

    assert initial_call == first_call == second_call == third_call
    assert third_call != fourth_call


def test_arg_kwarg_for_cache():
    """
    Passes test if results of `function()` decorated by `@cache()` are stable.
    """

    @cache(times=2)
    def function(variable: int, multiplicator: int = 2):
        return (variable * multiplicator) + const

    const = 1
    initial_call = function(1)

    const = 2
    first_call = function(1)

    second_call = function(1)

    third_call = function(1)

    assert initial_call == first_call == second_call != third_call


def test_value_error_for_cache():
    """
    Passes test if `ValueError` with `NON_VALID_TIMES` message
    is raised if `function` decorated by `@cache(times=0)`.
    """
    with pytest.raises(ValueError) as exception_info:

        @cache(times=0)
        def function(value):
            return value

        function(1)

    assert str(exception_info.value) == NON_VALID_TIMES
