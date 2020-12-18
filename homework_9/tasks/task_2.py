"""
Write a context manager, that suppresses passed exception.
Do it both ways: as a class and as a generator.
```

>>> with supressor(IndexError):
...    [][2]

```
"""
from contextlib import contextmanager

# https://stackoverflow.com/questions/1549801


class Supressor:
    """
    Context manager class which suppresses `exception`.

    Suppressing maintains an exceptions hierarchy:
    ```

    >>> with Supressor(IndexError):
    ...    [][2]

    >>> with Supressor(Exception):
    ...    [][2]

    ```
    """

    def __init__(self, exception: Exception):
        self.__exception = exception

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_value, traceback):
        return isinstance(exc_value, self.__exception)


@contextmanager
def supressor(exception: Exception):
    """
    Context manager function which suppresses `exception`.

    Suppressing maintains an exceptions hierarchy:
    ```

    >>> with supressor(IndexError):
    ...    [][2]

    >>> with supressor(Exception):
    ...    [][2]

    ```
    """
    try:
        yield
    except exception as current:
        if not isinstance(current, exception):
            raise current
