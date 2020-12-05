"""
Unit tests for `backspace_compare` from module `homework_7.tasks.task_2`.
"""
import pytest

from homework_7.tasks.task_2 import backspace_compare


@pytest.mark.parametrize(
    ["first", "second"],
    [
        pytest.param("a", "##a", id="a->a, ##a->a"),
        pytest.param("##a", "a", id="##a->a, a->a"),
        pytest.param("ab#c", "ad#c", id="ab#c->ac, ad#c->ac"),
        pytest.param("a##c", "#a#c", id="a##c->c, #a#c->c"),
    ],
)
def test_common_true(first: str, second: str):
    """Passes test if `backspace_compare(first, second)` is `True`."""
    assert backspace_compare(first, second)


@pytest.mark.parametrize(
    ["first", "second"],
    [
        pytest.param("a#c", "b", id="a#c->c, b->b"),
        pytest.param("a#c#d", "e#f#g", id="a#c#d->d, e#f#g->g"),
    ],
)
def test_common_false(first: str, second: str):
    """Passes test if `backspace_compare(first, second)` is `False`."""
    assert backspace_compare(first, second) is False


@pytest.mark.parametrize(
    ["first", "second"],
    [
        pytest.param("", "", id="Empty strings: '' and ''."),
        pytest.param("###", "###", id="Empty strings: '###' and '###'."),
        pytest.param("###", "", id="Empty strings: '###' and ''."),
        pytest.param("", "###", id="Empty strings: '' and '###'."),
        pytest.param("###", "#", id="Empty strings: '###' and '#'."),
        pytest.param("#", "###", id="Empty strings: '#' and '###'."),
        pytest.param("a#b#c#", "d#e#f#", id="Empty strings: 'a#b#c#' and 'd#e#f#'."),
    ],
)
def test_empty_strings_true(first: str, second: str):
    """Passes test if `backspace_compare(first, second)` is `True`."""
    assert backspace_compare(first, second)


@pytest.mark.parametrize(
    ["first", "second"],
    [
        pytest.param("", "a", id="''->'', a->a"),
        pytest.param("a", "", id="a->a, ''->''"),
        pytest.param("#", "a", id="'#'->'', a->a"),
        pytest.param("a", "#", id="a->a, '#'->''"),
    ],
)
def test_empty_strings_false(first: str, second: str):
    """Passes test if `backspace_compare(first, second)` is `False`."""
    assert backspace_compare(first, second) is False
