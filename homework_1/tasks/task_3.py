"""
Write down the function, which reads input line-by-line, and find maximum and minimum values.
Function should return a tuple with the max and min values.

For example for [1, 2, 3, 4, 5], function should return [1, 5]

We guarantee, that file exists and contains line-delimited integers.

To read file line-by-line you can use this snippet:

with open("some_file.txt") as fi:
    for line in fi:
        ...

"""
from typing import Tuple


def find_maximum_and_minimum(file_name: str) -> Tuple[int, int]:
    """
    Returns tuple with the min and max `int` from `file_name`.

    Requirements:
    -------------
    `file_name` should exist and contains line-delimited integers.
    """
    with open(file=file_name, mode="rt") as file:
        numbers = [int(line.strip()) for line in file]
    return min(numbers), max(numbers)
