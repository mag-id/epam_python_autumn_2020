"""
Given a list of integers numbers "nums".

You need to find a sub-array with length less equal to "k", with maximal sum.

The written function should return the sum of this sub-array.

Examples:
    nums = [1, 3, -1, -3, 5, 3, 6, 7], k = 3
    result = 16
"""
from typing import List

INDEX_ERROR_TEXT = "Length of the input list must be > 0."
VALUE_ERROR_TEXT = "Maximal subarray length must be > 0."


def find_maximal_subarray_sum(array: List[int], max_subarray_length: int) -> int:
    """
    Returns maximal sum of subarray with length <= `max_subarray_length` from `array`.
    Based on [Kadane's algorithm](https://en.wikipedia.org/wiki/Maximum_subarray_problem).

    If len(`array`) <= 0 - `IndexError` will raise.
    If `max_subarray_length` <= 0 - `ValueError` will raise.
    """

    if not array:
        raise IndexError(INDEX_ERROR_TEXT)

    if max_subarray_length <= 0:
        raise ValueError(VALUE_ERROR_TEXT)

    best_sum = float("-inf")
    current_sum = 0

    for end, value in enumerate(array):

        if current_sum <= 0:
            current_sum = value
            start = end
        else:
            current_sum += value

        if end - start == max_subarray_length:
            current_sum -= array[start]
            start += 1

        if current_sum > best_sum:
            best_sum = current_sum

    return best_sum
