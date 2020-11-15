"""
Some of the functions have a bit cumbersome behavior when we deal with
positional and keyword arguments.

Write a function that accept any iterable of unique values and then
it behaves as range function:


import string


assert = custom_range(string.ascii_lowercase, 'g') == ['a', 'b', 'c', 'd', 'e', 'f']
assert = custom_range(string.ascii_lowercase, 'g', 'p') == [
    'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o'
]
assert = custom_range(string.ascii_lowercase, 'p', 'g', -2) == ['p', 'n', 'l', 'j', 'h']

"""
from typing import Any, Iterable, List


def custom_range(
    unique_values: Iterable[Any],
    required_border: Any,
    optional_border: Any = None,
    step: int = 1,
) -> List[Any]:
    """
    Returns list of values from `unique_values` according to the built-in `range` behaviour.
    If `start`, `stop`, and `step` are not specified, list of `unique_values` will returned.
    """
    collected = list(unique_values)

    if not optional_border:
        start = 0
        stop = collected.index(required_border)
    else:
        start = collected.index(required_border)
        stop = collected.index(optional_border)

    if step < 0:
        start, stop = stop, start

    return [collected[index] for index in range(start, stop, step)]
