"""
save_original_info.py
---------------------

Написать декоратор который позволит сохранять информацию из
исходной функции (__name__ and __doc__), а так же сохранит саму
исходную функцию в атрибуте __original_func

print_result изменять нельзя, за исключением добавления вашего
декоратора на строку отведенную под него - замените комментарий

До применения вашего декоратор будет вызываться AttributeError при custom_sum.__original_func
Это корректное поведение
После применения там должна быть исходная функция

Ожидаемый результат:
print(custom_sum.__doc__)  # 'This function can sum any objects which have __add___'
print(custom_sum.__name__)  # 'custom_sum'
print(custom_sum.__original_func)  # <function custom_sum at <some_id>>
"""
from functools import wraps
from typing import Callable


def extended_wraps(wrapped: Callable) -> Callable:
    """
    Decorates a wrapper function for looking like the `wrapped` function.
    Works like [functools.wraps
    ](https://docs.python.org/3.8/library/functools.html#functools.wraps), but
    also has `__original_func` attribute which store the original function object.
    """
    wrapped.__dict__.update({"__original_func": wrapped})
    return wraps(
        wrapped=wrapped,
        assigned=("__name__", "__doc__"),
        updated=("__dict__",),
    )
