"""
Unit tests for module `homework_3.tasks.task_3`.
"""

# pylint: disable=redefined-outer-name

from typing import Any, Callable, Dict, List, Tuple

import pytest

from homework_3.tasks.task_3 import NON_VALID_VALUE, SAMPLE_DATA, Filter, make_filter


@pytest.fixture()
def good_instance():
    """
    Returns `Filter` instance with the
    correct order of the functions.
    """
    return Filter(
        lambda a: isinstance(a, int),
        lambda a: a % 2 == 0,
        lambda a: a > 0,
    )


@pytest.fixture()
def empty_instance():
    """
    Returns `Filter` instance with no functions.
    """
    return Filter()


@pytest.fixture()
def bad_instance():
    """
    Returns `Filter` instance with
    wrong order of the functions.
    """
    return Filter(
        lambda a: a % 2 == 0,
        lambda a: a > 0,
        lambda a: isinstance(a, int),
    )


class TestFilter:
    """Just wraps tests for `Filter` class."""

    @staticmethod
    @pytest.mark.parametrize(
        ["functions"],
        [
            pytest.param(
                (
                    lambda a: a % 2 == 0,
                    lambda a: a > 0,
                    lambda a: isinstance(a, int),
                ),
                id="Positive: the instance of Filter class is created.",
            ),
            pytest.param(
                (
                    lambda a: isinstance(a, int),
                    lambda a: a > 0,
                    lambda a: a % 2 == 0,
                ),
                id="Positive: the instance of Filter class is created.",
            ),
            pytest.param(
                (lambda a: a % 2 == 0,),
                id="Positive: the instance of Filter class is created.",
            ),
        ],
    )
    def test_positive_initialization(functions: Tuple[Callable]):
        """Passes test if the instance of the `Filter` class is created."""
        assert isinstance(Filter(*functions), Filter)

    @staticmethod
    @pytest.mark.parametrize(
        ["functions", "expected_exception", "expected_message"],
        [
            pytest.param(
                (
                    lambda: True,
                    lambda: False,
                ),
                ValueError,
                NON_VALID_VALUE,
                id="Negative: functions without arguments.",
            ),
            pytest.param(
                (
                    lambda a, b: a == b,
                    lambda a, b: a == b,
                ),
                ValueError,
                NON_VALID_VALUE,
                id="Negative: functions with multiple arguments.",
            ),
        ],
    )
    def test_negative_initialization(
        functions: Tuple[Callable], expected_exception: Exception, expected_message: str
    ):
        """Passes test if the `expected_exception` raises with `expected_message`."""
        with pytest.raises(expected_exception) as exception_info:
            Filter(*functions)
        assert str(exception_info.value) == expected_message

    @staticmethod
    @pytest.mark.parametrize(
        ["data", "expected_result"],
        [
            pytest.param(
                list(range(100)),
                list(range(2, 100, 2)),
                id="Positive: should return list with only even numbers from 0 to 99.",
            ),
            pytest.param(
                list(range(1, 100, 2)),
                [],
                id="Positive: should return an empty list.",
            ),
            pytest.param(
                list(range(-100, 0)),
                [],
                id="Positive: should return an empty list.",
            ),
            pytest.param(
                ["a", "b", "c", "d"],
                [],
                id="Positive: should return an empty list.",
            ),
        ],
    )
    def test_positive_apply(good_instance, data: Any, expected_result: Any):
        """
        Passes test if for `good_instance.apply(data)` is equal to `expected_result`.
        """
        assert good_instance.apply(data) == expected_result

    @staticmethod
    @pytest.mark.parametrize(
        ["data", "expected_result"],
        [
            pytest.param(
                SAMPLE_DATA,
                SAMPLE_DATA,
                id="Boundary: should return same data.",
            ),
        ],
    )
    def test_bondary_apply(empty_instance, data: Any, expected_result: Any):
        """
        Passes test if for `empty_instance.apply(data)` is equal to `expected_result`.
        """
        assert empty_instance.apply(data) == expected_result

    @staticmethod
    @pytest.mark.parametrize(
        ["data", "expected_exception", "expected_message"],
        [
            pytest.param(
                ["a", "b", "c", "d"],
                TypeError,
                "not all arguments converted during string formatting",
                id="Negative: wrong order of the functions inside the instance.",
            ),
        ],
    )
    def test_negative_apply(
        bad_instance, data: Any, expected_exception: Exception, expected_message: str
    ):
        """Passes test if the `expected_exception` raises with `expected_message`."""
        with pytest.raises(expected_exception) as exeception_info:
            bad_instance.apply(data)
        assert str(exeception_info.value) == expected_message


@pytest.mark.parametrize(
    ["keywords", "data", "expected_result"],
    [
        pytest.param(
            {
                "name": "polly",
                "type": "bird",
            },
            SAMPLE_DATA,
            [
                SAMPLE_DATA[1],
            ],
            id="Positive: should return list with 2nd entry from SAMPLE_DATA.",
        ),
        pytest.param(
            {
                "name": "Bill",
            },
            SAMPLE_DATA,
            [
                SAMPLE_DATA[0],
            ],
            id="Positive: should return list with 1st entry from SAMPLE_DATA.",
        ),
        pytest.param(
            {
                "name": True,
                "type": int,
            },
            SAMPLE_DATA,
            [],
            id="Positive: should return an empty list.",
        ),
        pytest.param(
            {
                "name": ["Bill", "polly"],
            },
            SAMPLE_DATA,
            [],
            id="Positive: should return an empty list.",
        ),
    ],
)
def test_positive_make_filter(
    keywords: Dict[str, Any],
    data: List[Dict[str, Any]],
    expected_result: List[Dict[str, Any]],
):
    """
    Passes test if for `make_filter(keywords).apply(data)` is equal to `expected_result`.
    """
    assert make_filter(**keywords).apply(data) == expected_result


@pytest.mark.parametrize(
    ["keywords", "data", "expected_result"],
    [
        pytest.param(
            {"nokey": None},
            SAMPLE_DATA,
            [],
            id="Boundary: should return an empty list.",
        ),
        pytest.param(
            {},
            SAMPLE_DATA,
            SAMPLE_DATA,
            id="Boundary: should return an empty list.",
        ),
    ],
)
def test_boundary_make_filter(
    keywords: Dict[str, Any],
    data: List[Dict[str, Any]],
    expected_result: List[Dict[str, Any]],
):
    """
    Passes test if for `make_filter(keywords).apply(data)` is equal to `expected_result`.
    """
    assert make_filter(**keywords).apply(data) == expected_result
