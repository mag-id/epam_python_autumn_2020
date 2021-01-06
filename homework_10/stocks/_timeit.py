"""Decorator which prints time of execution."""

from time import time
from typing import Callable

__all__ = ["timeit"]


def timeit(call: Callable):
    """
    Decorator which prints time of execution in format like:
    ```
    TIMEIT: <function main at 0x100f17310> execution = 564.2723650932312 sec.
    ```
    """

    def timed(*args, **kwargs):
        start = time()
        result = call(*args, **kwargs)
        end = time()
        print(f"TIMEIT: {call} execution = {end - start} sec.")
        return result

    return timed
