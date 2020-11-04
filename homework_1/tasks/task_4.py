"""
Classic task, a kind of walnut for you

Given four lists A, B, C, D of integer values,
compute how many tuples (i, j, k, l) there are such that A[i] + B[j] + C[k] + D[l] is zero.

We guarantee, that all A, B, C, D have same length of N where 0 ≤ N ≤ 1000.
"""
from itertools import product
from typing import List


def check_sum_of_four(
    a_values: List[int], b_values: List[int], c_values: List[int], d_values: List[int]
) -> int:
    """
    Returns number of zero-sum tuples (`a_entry`, `b_entry`, `c_entry`, `d_entry`)
    which are constructed from `a_values`, `b_values`, `c_values`, `d_values`.

    Requirements:
    -------------
    `a_values`, `b_values`, `c_values`, `d_values` have same length N, where 0 ≤ N ≤ 1000.
    """
    return [
        sum(entries) for entries in product(a_values, b_values, c_values, d_values)
    ].count(0)
