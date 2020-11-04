"""
Functions of the `sample_project.calculator.calc` module.
"""


def check_power_of_2(value: int) -> bool:
    """
    Returns `True` if `value` is power of 2 else `False`.
    See code explanation in [StackOverflow
    ](https://stackoverflow.com/questions/57025836).
    """
    return (value != 0) and (not value & (value - 1))
