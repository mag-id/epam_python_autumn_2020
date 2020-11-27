"""Unit tests for `extended_wraps` decorator from module `homework_5.tasks.task_2`."""

from functools import reduce
from typing import Any, Callable

import pytest

from homework_5.tasks.task_2 import extended_wraps

ARGUMENTS = 1, 2, 3, 4


def helper_custom_sum(*args: Any) -> Any:
    """
    This function can sum any objects which have `__add___`.
    """
    return reduce(lambda x, y: x + y, args)


def helper_decorate(func: Callable) -> Callable:
    """
    Returns the function wrapped in decorator for printing result of the `func`.
    Also, the wrapper is wrapped by the current test `extended_wraps` decorator.
    """

    def print_result(func: Callable) -> Callable:
        """
        Decorator for printing result of an original function.
        """

        @extended_wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            """
            Function-wrapper which prints result of an original function.
            """
            result = func(*args, **kwargs)
            print(result)
            return result

        return wrapper

    return print_result(func)


# pylint: disable=W0621
@pytest.fixture
def prepared_helpers() -> Callable:
    """Returns decorated helper functions."""
    return helper_decorate(helper_custom_sum)


def test_attributes(prepared_helpers):
    """
    Passes test if attributes of the `helper_custom_sum`
    are equal to attributes of the `prepared_helpers`.
    """
    assert (prepared_helpers.__name__, prepared_helpers.__doc__) == (
        helper_custom_sum.__name__,
        helper_custom_sum.__doc__,
    )


def test_wrapper_side_effects(capsys, prepared_helpers):
    """
    Passes test if `prepared_helpers` prints and returns result.
    """
    wrapped_result = prepared_helpers(*ARGUMENTS)
    helper_result = helper_custom_sum(*ARGUMENTS)
    out, err = capsys.readouterr()

    assert (out, err) == (f"{wrapped_result}\n", "")
    assert helper_result == wrapped_result


def test_unbound_method(capsys, prepared_helpers):
    """
    Passes test if `prepared_helpers.__original_func`
    is `helper_custom_sum` and behaves like `helper_custom_sum`.
    """
    unbounded = prepared_helpers.__original_func  # pylint: disable=W0212
    out, err = capsys.readouterr()

    assert unbounded is helper_custom_sum
    assert (out, err) == ("", "")
