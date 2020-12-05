"""
Given a dictionary (tree), that can contains multiple nested structures.
Write a function, that takes element and finds the number of occurrences
of this element in the tree.

Tree can only contains basic structures like:
    str, list, tuple, dict, set, int, bool
"""
from typing import Any


def find_occurrences(tree: dict, element: Any) -> int:
    """Returns number of `element` in `tree`."""
    return _check(tree, element, occurrences=0)


def _check(node: Any, element: Any, occurrences: int) -> int:
    """
    Recursively increases `occurrences` of the `element`
    in `node` and returns final `occurrences`.
    """
    if isinstance(node, dict):
        for key, value in node.items():
            occurrences = _check(key, element, occurrences)
            occurrences = _check(value, element, occurrences)

    elif isinstance(node, (set, list, tuple)):
        for item in node:
            occurrences = _check(item, element, occurrences)

    else:
        if node == element:
            occurrences += 1

    return occurrences
