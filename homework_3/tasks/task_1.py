"""
In previous homework task 4, you wrote a cache function that remembers other function output value.
Modify it to be a parametrized decorator, so that the following code::

    @cache(times=3)
    def some_function():
        pass


Would give out cached value up to `times` number only.
Example::

    @cache(times=2)
    def f():
        return input('? ')   # careful with input() in python2, use raw_input() instead

    >>> f()
    ? 1
    '1'
    >>> f()     # will remember previous value
    '1'
    >>> f()     # but use it up to two times only
    '1'
    >>> f()
    ? 2
    '2'
"""
from typing import Callable

NON_VALID_TIMES = "times must be > 0."


def cache(times=3) -> Callable:
    """
    Accepts `function` and returns a result.
    If `args`, `kwargs` were called before -
    returns corresponded result from cache.

    Cached result removed if it was call
    more than `times`, by default `times = 3`.

    If `times` < 1, `ValueError("times must be > 0.")`
    will be raised.
    """
    cached, timing = {}, {}

    if times < 1:
        raise ValueError(NON_VALID_TIMES)

    def decorate(function: Callable):
        def listen(*args, **kwargs):
            """
            Listens `args`, `kwargs` and return an answer.
            Tracks how much `times` answer called.
            """
            call = f"[{args},{kwargs}]"

            if call in timing:
                answer = cached[call]

                if timing[call] == 1:
                    del timing[call]
                    del cached[call]
                else:
                    timing[call] -= 1
                return answer

            answer = function(*args, **kwargs)
            timing[call] = times
            cached[call] = answer
            return answer

        return listen

    return decorate
