"""
Write a function that gets file path as an argument.
Read the first line of the file.
If first line is a number return true if number in an interval [1, 3)*
and false otherwise.
In case of any error, a ValueError should be thrown.

Write a test for that function using pytest library.

Definition of done:
 - function is created
 - function is properly formatted
 - function has positive and negative tests
 - all temporary files are removed after test run

You will learn:
 - how to test Exceptional cases
 - how to clean up after tests
 - how to check if file exists**
 - how to handle*** and raise**** exceptions in test. Use sample from the documentation.

* https://en.wikipedia.org/wiki/Interval_(mathematics)#Terminology
** https://docs.python.org/3/library/os.path.html
*** https://docs.python.org/3/tutorial/errors.html#handling-exceptions
**** https://docs.python.org/3/tutorial/errors.html#raising-exceptions
"""

from os import F_OK, R_OK, access

NOT_EXIST = "Path is not exists."
NOT_READABLE = "Path is not readable."


def read_magic_number(path: str) -> bool:
    """
    Returns `True` if first line of file in `path` is
    number where in range 1 <= number < 3 else `False`.

    Exceptions:
    -----------
    + If the file does not exist then `ValueError(Path does not exist.)` raises.
    + If the file is not readable then `ValueError(Path is not readable.)` raises.
    """
    if not access(path, F_OK):
        raise ValueError(NOT_EXIST)

    if not access(path, R_OK):
        raise ValueError(NOT_READABLE)

    with open(file=path, mode="tr", encoding="utf-8") as file:
        first_line = file.readline().strip()

        prepared = first_line.replace(",", ".", 1)
        replased = prepared.replace(".", "", 1)

        return replased.isdigit() and (1.0 <= float(prepared) < 3.0)
