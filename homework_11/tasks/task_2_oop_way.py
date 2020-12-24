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

# pylint: disable=too-few-public-methods


class Discount(ABC):
    """
    Strategy interface.

    Implements `calculate` staticmethod for logic executing.
    """

    @staticmethod
    def calculate(order: "Order", percentage: float) -> int:
        """
        Returns final price of the `order`
        according to current `percentage`.
        """
        return int(order.price - order.price * percentage)


class MorningDiscount:
    """
    `MorningDiscount` is 50%.
    """

    @staticmethod
    def calculate(order: "Order") -> int:
        """
        Returns final price of the
        `order` with a 50% discount.
        """
        return Discount.calculate(order, 0.5)


class ElderDiscount:
    """
    `ElderDiscount` is 90%.
    """

    @staticmethod
    def calculate(order: "Order") -> int:
        """
        Returns final price of the
        `order` with a 90% discount.
        """
        return Discount.calculate(order, 0.9)


class Order:
    """
    Context class.

    Takes `price` and `discount`.
    Implements `final_price` method.

    Example:
    --------
    ```
    >>> morning_discount = MorningDiscount()
    >>> elder_discount = ElderDiscount()

    >>> order_1 = Order(100, morning_discount)
    >>> assert order_1.final_price() == 50

    >>> order_2 = Order(100, elder_discount)
    >>> assert order_2.final_price() == 10

    ```
    """

    def __init__(self, price: int, discount: Discount):
        self.__price = price
        self.__discount = discount

    @property
    def price(self) -> int:
        """
        Returns initial `price`.
        """
        return self.__price

    def final_price(self) -> int:
        """
        Returns final price of the current `Order`.
        """
        return self.__discount.calculate(self)
