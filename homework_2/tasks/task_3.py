"""
Write a function that takes K lists as arguments and returns all possible
lists of K items where the first element is from the first list,
the second is from the second and so one.

You may assume that that every list contain at least one element

Example:

assert combinations([1, 2], [3, 4]) == [
    [1, 3],
    [1, 4],
    [2, 3],
    [2, 4],
]
"""
from itertools import product
from typing import Any, List


def combinations(*args: List[Any]) -> List[List]:
    """
    Takes N lists of any items as `*args` and returns lists
    with a possible combination of them as lists with length N,
    where the first item from the first list,
    the second item from the second list, and etc.

    Note:
    -----
    If any `[]` in `*args` then `[]` will be returned:
    ```

    >>> combinations([], [])
    []

    >>> combinations([1, 2], [], [3])
    []

    ```
    """
    return [list(combination) for combination in product(*args)]
