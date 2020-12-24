"""
Realization of Task 2 in the OOP way.
=====================================

Task 2:
-------

You are given the following code:

class Order:
    morning_discount = 0.25

    def __init__(self, price):
        self.price = price

    def final_price(self):
        return self.price - self.price * self.morning_discount

Make it possible to use different discount programs.
Hint: use strategy behavioural OOP pattern.
https://refactoring.guru/design-patterns/strategy

Example of the result call:

def morning_discount(order):
    ...

def elder_discount(order):
    ...

order_1 = Order(100, morning_discount)
assert order_1.final_price() == 50

order_2 = Order(100, elder_discount)
assert order_1.final_price() == 10  # Maybe order_2 ?
"""

from abc import ABC
from typing import Any

# pylint: disable=too-few-public-methods


class Strategy(ABC):
    """
    Strategy interface implements `execute`
    classmethod which execute `Strategy` logic.
    """

    @classmethod
    def execute(cls, *args: Any, **kwargs: Any) -> Any:
        """
        Executes `Strategy` logic.
        """
        raise NotImplementedError


class Context:
    """
    Creates instance with next methods:
    + `set_strategy` - for setting `strategy` to the `Context`
    + `execute_strategy` - for executing `strategy` logic
    """

    def __init__(self):
        self.__strategy = None

    def set_strategy(self, strategy: Strategy):
        """
        Sets `strategy` to the `Context`.
        """
        self.__strategy = strategy

    def execute_strategy(self, *args: Any, **kwargs: Any) -> Any:
        """
        Executes current `strategy` logic in current `Context`.
        """
        return self.__strategy.execute(*args, **kwargs)


# pylint: disable=arguments-differ


class MorningDiscount(Strategy):
    """
    `MorningDiscount` is 50%.
    """

    __discount = 0.5

    @classmethod
    def execute(cls, price: int) -> int:
        """
        Returns new `price` according `MorningDiscount`: 50%.
        """
        return int(price - price * cls.__discount)


class ElderDiscount(Strategy):
    """
    `ElderDiscount` is 90%.
    """

    __discount = 0.9

    @classmethod
    def execute(cls, price: int) -> int:
        """
        Returns new `price` according `ElderDiscount`: 90%
        """
        return int(price - price * cls.__discount)


class Order:
    """
    Creates an instance with `price` and `discount`
    and implements `final_price` method.

    Example:
    --------
    ```

    >>> order_1 = Order(100, MorningDiscount)
    >>> assert order_1.final_price() == 50

    >>> order_2 = Order(100, ElderDiscount)
    >>> assert order_2.final_price() == 10

    ```
    """

    def __init__(self, price: int, discount: Strategy):
        self.__price = price

        self.__context = Context()
        self.__context.set_strategy(discount)

    def final_price(self) -> Any:
        """
        Returns final `price` of the `Order`.
        """
        return self.__context.execute_strategy(self.__price)
