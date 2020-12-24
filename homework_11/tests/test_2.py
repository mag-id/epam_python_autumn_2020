"""
Unit tests for `task_2_oop_way` and `task_2_pythonic_way`
from the `homework_11.tasks` module.
"""
from homework_11.tasks.task_2_oop_way import Discount
from homework_11.tasks.task_2_oop_way import Order as OrderOOP
from homework_11.tasks.task_2_pythonic_way import Order as OrderPythonic
from homework_11.tasks.task_2_pythonic_way import calculate_discount

# pylint: disable=too-few-public-methods


def test_oop():
    """
    Passes test if `Discount` and `OrderOOP` have predictable behaviour.
    """

    class CurrentDiscount:
        """Tests `Discount`."""

        @staticmethod
        def calculate(order: OrderOOP):
            """Tests `calculate`."""

            return Discount.calculate(order=order, percentage=0.1)

    order = OrderOOP(price=100, discount=CurrentDiscount)

    assert order.final_price() == 90


def test_pythonic():
    """
    Passes test if `calculate_discount` and `OrderPythonic` have predictable behaviour.
    """

    order = OrderPythonic(
        price=100,
        discount=lambda order: calculate_discount(order=order, percentage=0.1),
    )

    assert order.final_price() == 90
