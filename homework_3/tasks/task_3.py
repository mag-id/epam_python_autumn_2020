"""
There are multiple bugs in this code. Find them all and write tests for faulty cases.

Description:
------------
+ I decided to write a code that generates data
filtering object from a list of keyword parameters.
+ Example of usage:
```
> positive_even = Filter(
    lambda a: a % 2 == 0, lambda a: a > 0, lambda a: isinstance(int, a)
)
> positive_even.apply(range(100))  # should return only even numbers from 0 to 99
> make_filter(
    name='polly', type='bird'
).apply(SAMPLE_DATA)  # should return only 2nd entry from the list
```
"""

# pylint: disable=cell-var-from-loop
# pylint: disable=too-few-public-methods

from inspect import signature
from typing import Any, Callable, Dict, List, Tuple

SAMPLE_DATA = [
    {
        "name": "Bill",
        "last_name": "Gilbert",
        "occupation": "was here",
        "type": "person",
    },
    {"is_dead": True, "kind": "parrot", "type": "bird", "name": "polly"},
]

NON_VALID_VALUE = "Functions must have a single argument."


class Filter:
    # Not <some>, but <all> criteria.
    """
    Helper filter class. Accepts a list of single-argument functions
    that return `True` if an object in list conforms to all criteria.

    Available methods:
    + `apply`
    """

    def __init__(self, *functions: Callable):
        # Encapsulated: self.functions = functions
        self.__functions = self.__check_arguments(functions)

    def apply(self, data: List[Any]) -> List[Any]:
        """
        Returns list with confirmed `data` entries.
        """
        # Refactored: [item for item in data if all(i(item) for i in self.functions)]
        return [
            entry for entry in data if all(check(entry) for check in self.__functions)
        ]

    # Added: __check_arguments
    @staticmethod
    def __check_arguments(functions: Tuple[Callable]) -> Tuple[Callable]:
        """
        Returns functions if they are single-argument,
        else raises ValueError('Functions must have a single argument.').
        """
        for func in functions:
            if len(signature(func).parameters) != 1:
                raise ValueError(NON_VALID_VALUE)
        return functions


def make_filter(**keywords: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Generate filter a object for specified keywords.
    """
    return Filter(
        *[
            lambda entry: entry[key] == word if key in entry else False
            for key, word in keywords.items()
        ]
    )


# Refactored:
# def make_filter(**keywords)
#     filter_funcs = []
#     for key, value in keywords.items():  # `value` - unused variable.
#         def keyword_filter_func(value):  # As consequence - wrong binding or naming.
#             return value[key] == value  # No checking `key` existence.
#     filter_funcs.append(keyword_filter_func)
#     return Filter(filter_funcs)
