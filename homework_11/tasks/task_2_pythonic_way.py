"""
Realization of Task 2 in the Pythonic way.
==========================================

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

from typing import Callable


class Order:
    """
    Context class.

    Takes `price` and `discount`.
    Implements `final_price` method.

    Example:
    --------
    ```

    >>> order_1 = Order(100, morning_discount)
    >>> assert order_1.final_price() == 50

    >>> order_2 = Order(100, elder_discount)
    >>> assert order_2.final_price() == 10

    ```
    """

    def __init__(self, price: int, discount: Callable):
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
        return self.__discount(self)


def calculate_discount(order: Order, percentage: float) -> int:
    """
    Returns final price of the `order`
    according to current `percentage`.
    """
    return int(order.price - order.price * percentage)


def morning_discount(order: Order) -> int:
    """
    Returns final price of the
    `order` with a 50% discount.
    """
    return calculate_discount(order, 0.5)


def elder_discount(order: Order) -> int:
    """
    Returns final price of the
    `order` with a 90% discount.
    """
    return calculate_discount(order, 0.9)
