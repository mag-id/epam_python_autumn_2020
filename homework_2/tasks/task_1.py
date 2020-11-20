"""
Given a file containing text. Complete using only default collections:

1) Find 10 longest words consisting from largest amount of unique symbols

answer:
-------
Souveränitätsansprüche, symbolischsakramentale,
Kollektivschuldiger, Bevölkerungsabschub,
unmißverständliche, Werkstättenlandschaft,
Verwaltungsmaßnahme, Selbstverständlich,
unverhältnismäßig, Schicksalsfiguren

2) Find rarest symbol for document

answer:
-------
'(', ')', 'X', 'Y', 'î', '’', '‹', '›'

3) Count every punctuation char

answer:
-------
5475

4) Count every non ascii char

answer:
-------
2972


5) Find most common non ascii char for document

answer:
-------
'ä'
"""

from collections import namedtuple
from typing import Callable, Dict, Hashable, Iterable, Iterator, List
from unicodedata import category


def get_longest_diverse_words(file_path: str, encoding="unicode_escape") -> List[str]:
    """
    Returns from `file_path` the list with first 10 longest words
    consisting of the largest amount of unique symbols in descending order.
    Default `encoding` is `"unicode_escape"`.
    """
    Word = namedtuple("Word", ["char_counter", "len_counter", "string"])
    top_ten_word = set()

    for word in _yield_words_in_file(file_path, encoding):
        top_ten_word.add(
            Word(
                char_counter=len(set(list(word))),
                len_counter=len(word),
                string=word,
            )
        )
        if len(top_ten_word) == 11:
            top_ten_word.remove(min(top_ten_word))

    return [word.string for word in sorted(top_ten_word, reverse=True)]


def count_punctuation_chars(file_path: str, encoding="unicode_escape") -> int:
    """
    Returns the number of punctuation characters in `file_path`.
    Default `encoding` is `"unicode_escape"`.
    """
    return sum(
        _count(
            _yield_chars_in_file(file_path, encoding),
            filter_=lambda value: category(value).startswith("P"),
        ).values()
    )


def count_non_ascii_chars(file_path: str, encoding="unicode_escape") -> int:
    """
    Returns the number of non-ASCII characters in `file_path`.
    Default `encoding` is `"unicode_escape"`.
    """
    return sum(
        _count(
            _yield_chars_in_file(file_path, encoding),
            filter_=lambda value: not value.isascii(),
        ).values()
    )


def get_rarest_char(file_path: str, encoding="unicode_escape") -> List[str]:
    """
    Returns the list with the rarest symbols in `file_path`.
    Default `encoding` is `"unicode_escape"`.
    """
    counted = _count(_yield_chars_in_file(file_path, encoding))
    grouped = _switch_keys_and_values(counted)
    return sorted(grouped[min(grouped)])


def get_most_common_non_ascii_char(
    file_path: str, encoding="unicode_escape"
) -> List[str]:
    """
    Returns the list with most common non-ASCII character in `file_path`.
    Default `encoding` is `"unicode_escape"`.
    """
    counted = _count(
        _yield_chars_in_file(file_path, encoding),
        filter_=lambda value: not value.isascii(),
    )
    grouped = _switch_keys_and_values(counted)
    return sorted(grouped[max(grouped)])


def _count(
    values: Iterable[Hashable], filter_: Callable = lambda value: True
) -> Dict[Hashable, int]:
    """
    Returns dictionary where keys are unique `values` and values
    there are entry counters. Adding condition can be specified by
    `filter_` argument which `lambda value: True` by default.
    """
    counted = {}
    for value in values:
        if filter_(value):
            if value in counted:
                counted[value] += 1
            else:
                counted[value] = 1
    return counted


def _switch_keys_and_values(
    key_value: Dict[Hashable, int]
) -> Dict[int, List[Hashable]]:
    """
    Returns dictionary with switched key-value arguments
    where new values (old keys) stored in the list.
    """
    value_key = {}
    for key, value in key_value.items():
        if value not in value_key:
            value_key[value] = [key]
        else:
            value_key[value].append(key)
    return value_key


def _yield_words_in_file(path: str, encoding="unicode_escape") -> Iterator[str]:
    """
    Yields words from `path`. Default `encoding` is `"unicode_escape"`.

    Tokenization rules:
    -------------------
    + Words devide by spacing: "letter", " " -> "letter".
    + Words with dash: "letter", "-", "letter" -> "letter+letter".
    + Words with hyphenation: "letter", "-", "\\n", "letter" -> "letter+letter".
    """
    buffer = letters = is_cleaned = ""
    space_char, newline_char, dash_char = " ", "\n", "-"

    for char in _yield_chars_in_file(path, encoding):

        if char.isalpha():

            if buffer == dash_char:
                yield letters
                buffer = letters = is_cleaned
            letters += char

        elif char == newline_char and letters:

            if buffer == dash_char:
                buffer += newline_char
            else:
                yield letters
                buffer = letters = is_cleaned

        elif char == space_char and letters:
            yield letters
            buffer = letters = is_cleaned

        elif char == dash_char:
            buffer += char


def _yield_chars_in_file(path: str, encoding="unicode_escape") -> Iterator[str]:
    """
    Yields characters from `path`. Default `encoding` is `"unicode_escape"`.
    """
    with open(file=path, mode="tr", encoding=encoding) as text:
        for line in text:
            for char in line:
                yield char


if __name__ == "__main__":

    PATH = "homework_2/tasks/data.txt"
    print(
        f"1) {get_longest_diverse_words(PATH)}",
        f"2) {get_rarest_char(PATH)}",
        f"3) {count_punctuation_chars(PATH)}",
        f"4) {count_non_ascii_chars(PATH)}",
        f"5) {get_most_common_non_ascii_char(PATH)}",
        sep="\n",
    )
