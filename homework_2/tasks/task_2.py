"""
Given an array of size n, find the most common and the least common elements.
The most common element is the element that appears more than n // 2 times.
The least common element is the element that appears fewer than other.

You may assume that the array is non-empty and the most common element
always exist in the array.

Example 1:

Input: [3,2,3]
Output: 3, 2

Example 2:

Input: [2,2,1,1,1,2,2]
Output: 2, 1

"""
from collections import Counter
from typing import List, Tuple

ARRAY_LENGTH_MESSAGE = "Length of the array must be > 3."
MOST_ELEMENT_MESSAGE = "The most common element is not defined."
LEAST_ELEMENT_MESSAGE = "The least common element is not defined."


def major_and_minor_elem(array: List[int]) -> Tuple[int, int]:
    """
    Returns the one most and the one least common element in `array`.

    Requirements:
    -------------
    + `array` length must be >= 3 or
    ValueError("Length of the array must be > 3.") will raises.

    + The most common element must exist or
    ValueError("The most common element is not defined.") will raises.

    + The least common element must exist or
    ValueError("The least common element is not defined.") will raises.

    Definition:
    -----------
    + The most common element - appears more than half of array.
    + The least common element - appears fewer than others.
    """
    if len(array) < 3:
        raise ValueError(ARRAY_LENGTH_MESSAGE)

    counted = Counter(array).most_common()
    most_element, most_counter = counted[0]

    if most_counter <= len(array) // 2:
        raise ValueError(MOST_ELEMENT_MESSAGE)

    least_element, least_counter = counted.pop()

    if len(counted) == 0 or least_counter in list(map(lambda pair: pair[1], counted)):
        raise ValueError(LEAST_ELEMENT_MESSAGE)

    return most_element, least_element
