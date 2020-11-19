"""
Write a function that takes a number N as an input and returns N FizzBuzz numbers*
Write a doctest for that function.
Write a detailed instruction how to run doctests**.

That how first steps for the instruction may look like:
 - Install Python 3.8 (https://www.python.org/downloads/)
 - Install pytest `pip install pytest`
 - Clone the repository <path your repository>
 - Checkout branch <your branch>
 - Open terminal
 - ...


Definition of done:
 - function is created
 - function is properly formatted
 - function has doctests
 - instructions how to run doctest with the pytest are provided

You will learn:
 - the most common test task for developers
 - how to write doctests
 - how to run doctests
 - how to write instructions

```

>>> fizzbuzz(5)
['1', '2', 'fizz', '4', 'buzz']

```

* https://en.wikipedia.org/wiki/Fizz_buzz
** Энциклопедия профессора Фортрана page 14, 15, "Робот Фортран, чисть картошку!"
"""
from typing import List


def fizzbuzz(counter: int) -> List[str]:
    """
    Returns list of fizzbuzz numbers in the range from 1 to `counter` inclusive.

    + Example of usage (doctest):
    ```

    >>> fizzbuzz(5)
    ['1', '2', 'fizz', '4', 'buzz']
    >>> fizzbuzz(15)[9:]
    ['buzz', '11', 'fizz', '13', '14', 'fizzbuzz']

    ```

    + How to run doctest:
    `$ pytest --doctest-modules homework_4/tasks/task_4.py`
    or
    `python homework_4/tasks/task_4.py -v`
    """
    numbers = []
    for number in range(1, counter + 1):
        fizz_or_buzz = ""

        if number % 3 == 0:
            fizz_or_buzz += "fizz"

        if number % 5 == 0:
            fizz_or_buzz += "buzz"

        numbers.append(fizz_or_buzz or str(number))

    return numbers


if __name__ == "__main__":
    import doctest

    doctest.testmod()
