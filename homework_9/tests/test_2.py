"""Unit tests for module `homework_9.tasks.task_2`."""
import pytest

from homework_9.tasks.task_2 import Supressor, supressor


# https://stackoverflow.com/questions/26266481
@pytest.fixture(params=[Supressor, supressor])
def suppressor_implementation(request):
    """
    Returns `Supressor` and `supressor` implementations.
    """
    return request.param


# pylint: disable=redefined-outer-name


def test_index_error(suppressor_implementation):
    """
    Passes test if `IndexError` suppresses.
    """
    with suppressor_implementation(IndexError):
        _ = [][2]


def test_no_index_error(suppressor_implementation):
    """
    Passes test if `IndexError` not occurs.
    """
    with suppressor_implementation(IndexError):
        _ = [0, 0, 0][2]


def test_another_error(suppressor_implementation):
    """
    Passes test if instead `ValueError`, `IndexError` occurs.
    """
    with pytest.raises(IndexError):
        with suppressor_implementation(ValueError):
            _ = [][2]


def test_exception(suppressor_implementation):
    """
    Passes test if `Exception` can catch `IndexError`.
    """
    with suppressor_implementation(Exception):
        _ = [][2]
