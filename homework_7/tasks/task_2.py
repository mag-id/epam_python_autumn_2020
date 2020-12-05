"""
Given two strings. Return if they are equal when both are typed into
empty text editors. # means a backspace character.

Note that after backspacing an empty text, the text will continue empty.

Examples:
    Input: s = "ab#c", t = "ad#c"
    Output: True
    # Both s and t become "ac".

    Input: s = "a##c", t = "#a#c"
    Output: True
    Explanation: Both s and t become "c".

    Input: a = "a#c", t = "b"
    Output: False
    Explanation: s becomes "c" while t becomes "b".
"""
from typing import List

BACKSPACE = "#"


def backspace_compare(first: str, second: str) -> bool:
    """
    Compares `first` and `second` backspace strings.
    If the are equal returns `True` else `False`.
    """
    return _get_characters(first) == _get_characters(second)


def _get_characters(string: str) -> List[str]:
    """Returns characters list from backspace `string`."""
    characters = []
    for char in string:

        if char != BACKSPACE:
            characters.append(char)
        elif characters:
            characters.pop()

    return characters
