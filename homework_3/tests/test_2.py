"""
Unit tests for module `homework_3.tasks.task_2`.
"""
from typing import Iterable

import pytest

from homework_3.tasks.task_2 import multiprocess_slow_calculate_sum, slow_calculate

PROCESSES = 61


@pytest.mark.parametrize(
    [
        "values",
    ],
    [
        pytest.param(range(1), id="values in range(1), result is 2785."),
        pytest.param(range(2), id="values in range(2), result is 4781."),
        pytest.param(range(3), id="values in range(3), result is 6428."),
    ],
)
def test_values_sum_multiprocess_slow_calculate_sum(values: Iterable[int]):
    """
    Passes test if sum of `slow_calculate`
    values and `multiprocess_slow_calculate_sum`
    with `PROCESSES` number of processes are equal.
    """
    assert sum(
        slow_calculate(value) for value in values
    ) == multiprocess_slow_calculate_sum(values, processes=PROCESSES)


@pytest.mark.timeout(60)
def test_time_execution_multiprocess_slow_calculate_sum():
    """
    Passes test if sum `multiprocess_slow_calculate_sum`
    with `PROCESSES` number of processes for range(500)
    gives correct answer [during 60 seconds
    ](https://pypi.org/project/pytest-timeout/).
    """
    assert multiprocess_slow_calculate_sum(range(500), processes=PROCESSES) == 1024259
