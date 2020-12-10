"""
Task 1
======

We have the `task1.txt` file that works as key-value storage,
each like is represented as key and value separated by `=` symbol, example:
```
name="kek"
last_name="top"
song_name="shadilay"
power=9001
```

Values can be strings or integer numbers.
If a value can be treated both as a number and a string, it is treated as number.

Write a wrapper class for this key value storage that works like this:
```
storage = KeyValueStorage("path_to_file.txt")
```

that has its keys and values accessible as collection items and as attributes.

```

# Example:
>>> PATH = "homework_8/tasks/task1.txt"
>>> storage = KeyValueStorage(PATH)
>>> assert storage["name"] == "kek"
>>> assert storage.song == "shadilay"
>>> assert storage.power == 9001

```

In case of attribute clash existing built-in attributes take precedence.
In case when value cannot be assigned to an attribute
(for example when there's a line `1=something`) `ValueError` should be raised.
File size is expected to be small, you are permitted to read it entirely into memory.
"""
from types import SimpleNamespace
from typing import Any, Dict

INVALID_PAIR = "Key-value pair can not be assigned."
INVALID_KEY = "Must be valid `str`."


# https://docs.python.org/3/library/types.html#types.SimpleNamespace
class KeyValueStorage(SimpleNamespace):
    """
    Parses key (as `str` only) value (as `int` or `str`) pairs
    according to `separator` (`"="` as default)
    from a text file at `path` with `encoding` (`"UTF-8"` as default)
    where data stored in `key{`separator`}value` lines format.

    Errors:
    -------
    + If numbers of `separator` in line != 1 - raises
    `ValueError :Key-value pair can not be assigned.`.

    + If the parsed key value is not a valid identifier - raises
    `ValueError: Must be valid `str`.`.

    + During (re)assignation of values or attributes - raises
    `TypeError: 'KeyValueStorage' object does not support item assignment`.
    """

    def __init__(self, path: str, separator: str = "=", encoding: str = "UTF-8"):
        super().__init__(**_parse(path, separator, encoding))

    def __getitem__(self, key: str):
        return self.__dict__[key]

    def __setattr__(self, key: Any, value: Any):
        raise TypeError(
            f"'{self.__class__.__name__}' object does not support item assignment"
        )


def _parse(path: str, separator: str, encoding: str) -> Dict[str, int or str]:
    """
    Returns key (as `str` only) value (as `int` or `str`) pairs
    according to `separator` from a text file at `path` with `encoding`
    where data stored in `key{`separator`}value` lines format.

    + If numbers of `separator` in line != 1 - raises
    `ValueError(INVALID_PAIR)`.

    + If the parsed key value is not a valid identifier - raises
    `ValueError(INVALID_PAIR)`.
    """
    with open(file=path, mode="r", encoding=encoding) as source:
        collected = {}
        for pair in source:

            if pair.count(separator) != 1:
                raise ValueError(INVALID_PAIR)

            key, value = pair.strip().split(separator)

            if not _check(key):
                raise ValueError(INVALID_KEY)

            if value.isdigit():
                value = int(value)

            collected.update({key: value})
        return collected


def _check(key: str) -> bool:
    """Returns `True` if `key` is valid identifier string else `False`."""
    return isinstance(key, str) and key.isidentifier()


if __name__ == "__main__":
    import doctest

    doctest.testmod()
