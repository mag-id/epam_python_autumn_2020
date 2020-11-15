"""
Here's a not very efficient calculation function that calculates something important::

    import time
    import struct
    import random
    import hashlib

    def slow_calculate(value):
        '''Some weird voodoo magic calculations'''
        time.sleep(random.randint(1,3))
        data = hashlib.md5(str(value).encode()).digest()
        return sum(struct.unpack('<' + 'B' * len(data), data))

Calculate total sum of slow_calculate() of all numbers starting from 0 to 500.
Calculation time should not take more than a minute.
Use functional capabilities of multiprocessing module.
You are not allowed to modify slow_calculate function.

answer:
-------
1024259
"""

import hashlib
import random
import struct
import time
from concurrent.futures import ProcessPoolExecutor
from typing import Iterable


# Don't modify
def slow_calculate(value):
    """Some weird voodoo magic calculations"""
    time.sleep(random.randint(1, 3))
    data = hashlib.md5(str(value).encode()).digest()
    return sum(struct.unpack("<" + "B" * len(data), data))


def multiprocess_slow_calculate_sum(
    values: Iterable[int], processes: int = None
) -> int:
    """
    Returns the sum of `slow_calculate(value)` in `values`.
    If `processes` is not specified, [then the default chosen
    will be at most `61`, even if more processors are available
    ](https://docs.python.org/3.8/library/concurrent.futures.html#processpoolexecutor).
    """
    with ProcessPoolExecutor(max_workers=processes) as executor:
        return sum(executor.map(slow_calculate, values))


if __name__ == "__main__":
    print(multiprocess_slow_calculate_sum(range(500)))
