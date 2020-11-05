"""
Given a list of integers numbers "nums".

You need to find a sub-array with length less equal to "k", with maximal sum.

The written function should return the sum of this sub-array.

Examples:
    nums = [1, 3, -1, -3, 5, 3, 6, 7], k = 3
    result = 16
"""
from typing import List


def find_maximal_subarray_sum(array: List[int], max_subarray_length: int) -> int:
    """
    Returns maximal sum of subarray with length <= `max_subarray_length` from `array`.
    Based on [Kadane's algorithm](https://en.wikipedia.org/wiki/Maximum_subarray_problem).
    """

    if not array:
        raise IndexError("len(array) must be > 0.")

    if max_subarray_length <= 0:
        raise ValueError("max_subarray_length must be > 0.")

    best_sum = current_sum = float("-inf")
    for current_end, value in enumerate(array):

        if current_sum <= 0:  # Start a new sequence at the current value.
            current_start = current_end
            current_sum = value
        else:  # Extend the existing sequence with the current value.
            current_sum += value

            # It is work as a queue:
            if (
                current_end - current_start == max_subarray_length
            ):  # if queue overflowed,
                current_sum -= array[current_start]  # remove the first value,
                current_start += 1  # reassign the first value.

        if current_sum > best_sum:
            best_sum = current_sum

    return best_sum
