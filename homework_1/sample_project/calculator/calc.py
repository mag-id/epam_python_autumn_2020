"""
Functions of the `sample_project.calculator.calc` module.
"""


def check_power_of_2(value: int) -> bool:
    """Returns `True` if `value` is power of 2 else `False`."""
    return not bool(value & (value - 1)) if value > 0 else False
