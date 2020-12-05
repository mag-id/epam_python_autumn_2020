"""
Unit tests for `find_occurrences` from module `homework_7.tasks.task_1`.
"""
from typing import Any

import pytest

from homework_7.tasks.task_1 import find_occurrences

EXAMPLE_TREE = {
    "first": ["RED", "BLUE"],
    "second": {
        "simple_key": ["simple", "list", "of", "RED", "valued"],
    },
    "third": {
        "abc": "BLUE",
        "jhl": "RED",
        "complex_key": {
            "key1": "value1",
            "key2": "RED",
            "key3": ["a", "lot", "of", "values", {"nested_key": "RED"}],
        },
    },
    "fourth": "RED",
}
TRICKY_TREE = {
    "string key": {1: True, 0: False},
    ("key", "tuple", "items"): [1, True, 0, False],
    (
        ("nested", "tuple"),
        "as",
        "key",
        "tuple",
        "items",
    ): {},
    True: 1,
    False: 0,
}


@pytest.mark.parametrize(
    ["tree", "element", "expected_result"],
    [
        pytest.param(EXAMPLE_TREE, "NO", 0, id="0 'NO' in `EXAMPLE_TREE`"),
        pytest.param(EXAMPLE_TREE, "RED", 6, id="6 'RED' in `EXAMPLE_TREE`"),
        pytest.param(EXAMPLE_TREE, "first", 1, id="1 'first' in `EXAMPLE_TREE`"),
        pytest.param(
            EXAMPLE_TREE, "simple_key", 1, id="1 'simple_key' in `EXAMPLE_TREE`"
        ),
        pytest.param(
            EXAMPLE_TREE, "complex_key", 1, id="1 'complex_key' in `EXAMPLE_TREE`"
        ),
        pytest.param(
            EXAMPLE_TREE, "nested_key", 1, id="1 'nested_key' in `EXAMPLE_TREE`"
        ),
    ],
)
def test_example_tree(tree: dict, element: Any, expected_result: int):
    """Passes test if `find_occurrences` result is equal to `expected_result`."""
    assert find_occurrences(tree, element) == expected_result


@pytest.mark.parametrize(
    ["tree", "element", "expected_result"],
    [
        pytest.param(TRICKY_TREE, "key", 2, id="2 `key` in `TRICKY_TREE`"),
        pytest.param(TRICKY_TREE, "items", 2, id="2 `items` in `TRICKY_TREE`"),
        pytest.param(TRICKY_TREE, "tuple", 3, id="2 `tuple` in `TRICKY_TREE`"),
        pytest.param(TRICKY_TREE, True, 6, id="6 `True` in `TRICKY_TREE`"),
        pytest.param(TRICKY_TREE, False, 6, id="6 `False` in `TRICKY_TREE`"),
        pytest.param(TRICKY_TREE, 1, 6, id="6 `1` in `TRICKY_TREE`"),
        pytest.param(TRICKY_TREE, 0, 6, id="6 `0` in `TRICKY_TREE`"),
    ],
)
def test_tricy_tree(tree: dict, element: Any, expected_result: int):
    """Passes test if `find_occurrences` result is equal to `expected_result`."""
    assert find_occurrences(tree, element) == expected_result
