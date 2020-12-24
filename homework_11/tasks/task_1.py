"""
Vasya implemented nonoptimal Enum classes.
Remove duplications in variables declarations using metaclasses.

from enum import Enum


class ColorsEnum(Enum):
    RED = "RED"
    BLUE = "BLUE"
    ORANGE = "ORANGE"
    BLACK = "BLACK"


class SizesEnum(Enum):
    XL = "XL"
    L = "L"
    M = "M"
    S = "S"
    XS = "XS"


Should become:

class ColorsEnum(metaclass=SimplifiedEnum):
    __keys = ("RED", "BLUE", "ORANGE", "BLACK")


class SizesEnum(metaclass=SimplifiedEnum):
    __keys = ("XL", "L", "M", "S", "XS")


assert ColorsEnum.RED == "RED"
assert SizesEnum.XL == "XL"
"""
from enum import Enum, EnumMeta
from typing import Any, Callable, Dict, Tuple

ITERABLE_CONAINER = "__keys"
INVALID_KEY = "Must be valid `str`."  # from homework_8.tasks.task_1


# https://stackoverflow.com/questions/54950379
class EnumDirectValueMixin(EnumMeta):
    """
    Mixin metaclass which allows having direct
    access to the `Enum` attributes values.
    """

    def __getattribute__(cls, attr: str) -> Any:
        collected = super().__getattribute__(attr)
        if isinstance(collected, cls):
            return collected.value
        return collected


class _SimplifiedEnum(Enum, metaclass=EnumDirectValueMixin):
    """Mixes `EnumDirectValueMixin` to the `Enum`."""


# https://www.python-course.eu/python3_metaclasses.php
class SimplifiedEnum(type):
    """
    Metaclass which allows defining `Enum` class like
    ```
    class SomeEnum(metaclass=SimplifiedEnum):
        __keys = args: Iterable[str]
    ```
    where
    ```
    SomeEnum.arg == "arg"
    ```

    Exapmle:
    --------
    ```

    >>> class ColorsEnum(metaclass=SimplifiedEnum):
    ...    __keys = ("RED", "BLUE", "ORANGE", "BLACK")
    >>> assert ColorsEnum.RED == "RED"

    >>> class _SizesEnum(metaclass=SimplifiedEnum):
    ...    __keys = ["XL", "L", "M", "S", "XS"]
    >>> assert _SizesEnum.XL == "XL"

    >>> class __BreakfastEnum(metaclass=SimplifiedEnum):
    ...    __keys = {"spam", "and", "eggs"}
    >>> assert __BreakfastEnum.eggs == "eggs"

    ```
    """

    def __new__(
        cls, name: str, _: Tuple[Callable], dict_: Dict[str, Any]
    ) -> _SimplifiedEnum:
        container_mask = f"_{name.lstrip('_')}{ITERABLE_CONAINER}"

        attributes = {}
        for key in dict_[container_mask]:

            if not _check(key):
                raise ValueError(INVALID_KEY)

            attributes.update({key: key})

        return _SimplifiedEnum(name, attributes)


# from homework_8.tasks.task_1
def _check(key: str) -> bool:
    """Returns `True` if `key` is valid identifier string else `False`."""
    return isinstance(key, str) and key.isidentifier()
