"""
oop_1.py
--------

Необходимо создать 3 класса и взаимосвязь между ними (Student, Teacher,
Homework)
Наследование в этой задаче использовать не нужно.
Для работы с временем использовать модуль datetime

1. Homework принимает на вход 2 атрибута: текст задания и количество дней
на это задание
Атрибуты:
    text - текст задания
    deadline - хранит объект datetime.timedelta с количеством
    дней на выполнение
    created - c точной датой и временем создания
Методы:
    is_active - проверяет не истело ли время на выполнение задания,
    возвращает boolean

2. Student
Атрибуты:
    last_name
    first_name
Методы:
    do_homework - принимает объект Homework и возвращает его же,
    если задание уже просрочено, то печатет 'You are late' и возвращает None

3. Teacher
Атрибуты:
     last_name
     first_name
Методы:
    create_homework - текст задания и количество дней на это задание,
    возвращает экземпляр Homework
    Обратите внимание, что для работы этого метода не требуется сам объект.

PEP8 соблюдать строго.
Всем перечисленным выше атрибутам и методам классов сохранить названия.
К названием остальных переменных, классов и тд. подходить ответственно -
давать логичные подходящие имена.

Example:
--------
```
teacher = Teacher('Daniil', 'Shadrin')
student = Student('Roman', 'Petrov')
print(teacher.last_name)  # Daniil
print(student.first_name)  # Petrov

expired_homework = teacher.create_homework('Learn functions', 0)
print(expired_homework.created)  # Example: 2019-05-26 16:44:30.688762
print(expired_homework.deadline)  # 0:00:00
print(expired_homework.text)  # 'Learn functions'

# create function from method and use it
create_homework_too = teacher.create_homework
oop_homework = create_homework_too('create 2 simple classes', 5)
print(oop_homework.deadline)  # 5 days, 0:00:00

student.do_homework(oop_homework)
student.do_homework(expired_homework)  # You are late
```
"""
from datetime import datetime, timedelta

LATE_MESSAGE = "You are late"
DAYS_MESSAGE = "Must be >= 0"


class Homework:
    """
    Takes `text` and `deadline` of the `Homework`.

    Attributes:
    -----------
    + `text` - text of the homework task.
    + `deadline` - available number of days for task completing.
    + `created` - date and time of homework creating.

    Methods:
    --------
    + `is_active` - returns `True` if the deadline is ok, else `False`.
    """

    def __init__(self, text: str, deadline: int):
        self.__text = text
        self.__deadline = timedelta(days=self.__check(deadline))
        self.__created = datetime.now()

    @property
    def text(self) -> str:
        """Returns `text`."""
        return self.__text

    @property
    def deadline(self) -> datetime:
        """Returns `deadline`."""
        return self.__deadline

    @property
    def created(self) -> datetime:
        """Returns `created`."""
        return self.__created

    def is_active(self) -> bool:
        """
        Check `deadline` with (current time - `created`) and
        returns `True` if the deadline is ok, else `False`.
        """
        return self.deadline > datetime.now() - self.created

    @staticmethod
    def __check(days: int) -> int:
        """
        Returns `days` if `days` > 0, else
        raise `ValueError("Must be > 0")`.
        """
        if days < 0:
            raise ValueError(DAYS_MESSAGE)
        return days


class Student:
    """
    Takes `last_name` and `first_name` of the `Student`.

    Attributes:
    -----------
    + `last_name`
    + `first_name`

    Methods:
    --------
    + `do_homework` - takes `Homework` instance,
    returns `Homework` if the deadline is ok, else `None` and prints 'You are late'.
    """

    def __init__(self, last_name: str, first_name: str):
        self.__last_name = last_name
        self.__first_name = first_name

    @property
    def last_name(self) -> str:
        """Returns `last_name`."""
        return self.__last_name

    @property
    def first_name(self) -> str:
        """Returns `first_name`."""
        return self.__first_name

    @staticmethod
    def do_homework(homework: Homework) -> Homework or None:
        """Returns `Homework` if the deadline is ok, else `None` and prints 'You are late'."""
        return homework if homework.is_active() else print(LATE_MESSAGE, end="")


class Teacher:
    """
    Takes `last_name` and `first_name` of the `Teacher`.

    Attributes:
    -----------
    + `last_name`
    + `first_name`

    Methods:
    --------
    + `create_homework` - takes `text` and `deadline`,
    returns `Homework` instance with `text` and `deadline`.
    """

    def __init__(self, last_name: str, first_name: str):
        self.__student = Student(last_name, first_name)

    @property
    def last_name(self) -> str:
        """Returns `last_name`."""
        return self.__student.last_name

    @property
    def first_name(self) -> str:
        """Returns `first_name`."""
        return self.__student.first_name

    @staticmethod
    def create_homework(text: str, deadline: int) -> Homework:
        """Returns `Homework` instance with `text` and `deadline`."""
        return Homework(text, deadline)


if __name__ == "__main__":

    teacher = Teacher("Daniil", "Shadrin")
    student = Student("Roman", "Petrov")
    print(teacher.last_name)  # Daniil
    print(student.first_name)  # Petrov

    expired_homework = teacher.create_homework("Learn functions", 0)
    print(expired_homework.created)  # Example: 2019-05-26 16:44:30.688762
    print(expired_homework.deadline)  # 0:00:00
    print(expired_homework.text)  # 'Learn functions'

    # create function from method and use it
    create_homework_too = teacher.create_homework
    oop_homework = create_homework_too("create 2 simple classes", 5)
    print(oop_homework.deadline)  # 5 days, 0:00:00

    student.do_homework(oop_homework)
    student.do_homework(expired_homework)  # You are late
