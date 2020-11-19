"""
This task is optional.

Write a generator that takes a number N as an input
and returns a generator that yields N FizzBuzz numbers*
Don't use any ifs, you can find an approach for the implementation in this video**.


Definition of done:
 - function is created
 - function is properly formatted
 - function has tests

```

>>> list(fizzbuzz(5))
['1', '2', 'fizz', '4', 'buzz']

```

* https://en.wikipedia.org/wiki/Fizz_buzz
** https://www.youtube.com/watch?v=NSzsYWckGd4
"""
from typing import Iterator


def fizzbuzz(counter: int) -> Iterator[str]:
    """
    Returns list of fizzbuzz numbers in the range from 1 to `counter` inclusive.

    + Example of usage (doctest):
    ```

    >>> list(fizzbuzz(5))
    ['1', '2', 'fizz', '4', 'buzz']
    >>> list(fizzbuzz(15))[9:]
    ['buzz', '11', 'fizz', '13', '14', 'fizzbuzz']

    ```

    + How to run doctest:
    `$ pytest --doctest-modules homework_4/tasks/task_4.py`
    or
    `python homework_4/tasks/task_4.py -v`
    """
    for number in range(1, counter + 1):
        fizz_or_buzz = (not number % 3 and "fizz") or ""  # pylint: disable=R1706
        fizz_or_buzz += (not number % 5 and "buzz") or ""  # pylint: disable=R1706
        yield fizz_or_buzz or str(number)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
