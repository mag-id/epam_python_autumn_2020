"""
counter.py
----------

Написать декоратор instances_counter, который применяется к любому классу
и добавляет ему 2 метода:
get_created_instances - возвращает количество созданых экземпляров класса
reset_instances_counter - сбросить счетчик экземпляров,
возвращает значение до сброса
Имя декоратора и методов не менять

Пример использования:
---------------------
```
User.get_created_instances()  # 0
user, _, _ = User(), User(), User()
user.get_created_instances()  # 3
user.reset_instances_counter()  # 3
```
"""
from abc import ABC


class CounterMixin(ABC):  # pylint: disable=R0903 (too-few-public-methods)
    """
    Counter mixin.

    Methods:
    + `_get_counter` - returns counter.
    + `_set_counter` - sets counter to the `number`.
    + `_increase_counter` - increase counter to the 1.
    """

    __counter: int = 0

    @classmethod
    def _get_counter(cls) -> int:
        """Returns counter."""
        return cls.__counter

    @classmethod
    def _set_counter(cls, number: int):
        """Sets counter to the `number`."""
        cls.__counter = number

    @classmethod
    def _increase_counter(cls):
        """
        Increase counter to the 1.

        Syntaxis sugar, the analogue of the:
        ```
        cls._set_counter(
            number = cls._get_counter - 1
        )
        ```
        """
        cls.__counter += 1


def instances_counter(cls):
    """
    Takes `cls` and returns `InstancesCounter` which counts each new instance.

    Also, adds two methods:
    + `get_created_instances` - returns number of created instances.
    + `reset_instances_counter` - returns the number of created instances and set it to `0`.
    """

    class InstancesCounter(cls, CounterMixin):
        """
        The mix of the inherited `cls` and `CounterMixin`.
        Increases counter for each new instance.
        """

        def __init__(self, *args, **kwargs):
            self._increase_counter()
            super().__init__(*args, **kwargs)

        @classmethod
        def get_created_instances(cls):
            """
            Returns the number of created instances.
            """
            return cls._get_counter()

        @classmethod
        def reset_instances_counter(cls):
            """
            Returns the number of created instances and set it to `0`.
            """
            current = cls._get_counter()
            cls._set_counter(0)
            return current

    return InstancesCounter
