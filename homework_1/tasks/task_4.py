"""
Classic task, a kind of walnut for you

Given four lists A, B, C, D of integer values,
compute how many tuples (i, j, k, l) there are
such that A[i] + B[j] + C[k] + D[l] is zero.

We guarantee, that all A, B, C, D have same length of N where 0 ≤ N ≤ 1000.
"""
from collections import Counter
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
    `a_values`, `b_values`, `c_values`, `d_values` have same length N,
    where 0 ≤ N ≤ 1000.

    Algorithm:
    ----------
    + Complexity O(N^4) simplified to O(N^2) by getting two arrays
    from all unique combinations in arrays pairs (ab and cd).
    + In the new two arrays, we count a number of identical sums.
    + For each equivalent, pair get a product of the counters
    (a i.m. number of combinations).
    + Finally, calculate the sum of all products (i.m. sum of all of the combinations).

    See [C++ realization](
        https://stackoverflow.com/questions/40575323/sum-of-4-integers-in-4-arrays).
    """
    ab_sum_counter = Counter(sum(pair) for pair in product(a_values, b_values))
    cd_sum_counter = Counter(sum(pair) for pair in product(c_values, d_values))
    return sum(
        ab_sum_counter[ab_sum] * cd_sum_counter[-ab_sum]
        for ab_sum in ab_sum_counter
        if -ab_sum in cd_sum_counter
    )
