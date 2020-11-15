"""
Write a function that accepts another function as an argument. Then it
should return such a function, so the every call to initial one
should be cached.


def func(a, b):
    return (a ** b) ** 2


cache_func = cache(func)

some = 100, 200

val_1 = cache_func(*some)
val_2 = cache_func(*some)

assert val_1 is val_2

"""
from typing import Callable


def cache(function: Callable) -> Callable:
    """
    Accepts `function` and returns a result.
    If `args`, `kwargs` were called before -
    returns corresponded result from cache.
    """
    cached = {}

    def listen(*args, **kwargs):
        """
        Listens `args`, `kwargs`
        and return an answer.
        """
        call = f"[{args},{kwargs}]"

        if call in cached:
            return cached[call]

        answer = function(*args, **kwargs)
        cached[call] = answer

        return answer

    return listen
