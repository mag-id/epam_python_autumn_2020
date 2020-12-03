"""
oop_2.py
--------

В этом задании будем улучшать нашу систему классов из задания прошлой лекции
(Student, Teacher, Homework)
Советую обратить внимание на defaultdict из модуля collection для
использования как общую переменную


1. Как то не правильно, что после do_homework мы возвращаем все тот же
объект - будем возвращать какой-то результат работы (HomeworkResult)

HomeworkResult принимает объект автора задания, принимает исходное задание
и его решение в виде строки
Атрибуты:
    homework - для объекта Homework, если передан не этот класс -  выкинуть
    подходящие по смыслу исключение с сообщением:
    'You gave a not Homework object'

    solution - хранит решение ДЗ как строку
    author - хранит объект Student
    created - c точной датой и временем создания

2. Если задание уже просрочено хотелось бы видеть исключение при do_homework,
а не просто принт 'You are late'.
Поднимайте исключение DeadlineError с сообщением 'You are late' вместо print.

3. Student и Teacher имеют одинаковые по смыслу атрибуты
(last_name, first_name) - избавиться от дублирования с помощью наследования

4.
Teacher
Атрибут:
    homework_done - структура с интерфейсом как в словаря, сюда поподают все
    HomeworkResult после успешного прохождения check_homework
    (нужно гаранитровать остутствие повторяющихся результатов по каждому
    заданию), группировать по экземплярам Homework.
    Общий для всех учителей. Вариант ипользования смотри в блоке if __main__...
Методы:
    check_homework - принимает экземпляр HomeworkResult и возвращает True если
    ответ студента больше 5 символов, так же при успешной проверке добавить в
    homework_done.
    Если меньше 5 символов - никуда не добавлять и вернуть False.

    reset_results - если передать экземпряр Homework - удаляет только
    результаты этого задания из homework_done, если ничего не передавать,
    то полностью обнулит homework_done.

PEP8 соблюдать строго.
Всем перечисленным выше атрибутам и методам классов сохранить названия.
К названием остальных переменных, классов и тд. подходить ответственно -
давать логичные подходящие имена.

Example:
--------
```
opp_teacher = Teacher('Daniil', 'Shadrin')
advanced_python_teacher = Teacher('Aleksandr', 'Smetanin')

lazy_student = Student('Roman', 'Petrov')
good_student = Student('Lev', 'Sokolov')

oop_hw = opp_teacher.create_homework('Learn OOP', 1)
docs_hw = opp_teacher.create_homework('Read docs', 5)

result_1 = good_student.do_homework(oop_hw, 'I have done this hw')
result_2 = good_student.do_homework(docs_hw, 'I have done this hw too')
result_3 = lazy_student.do_homework(docs_hw, 'done')

try:
    result_4 = HomeworkResult(good_student, "fff", "Solution")
except Exception:
    print('There was an exception here')

opp_teacher.check_homework(result_1)
temp_1 = opp_teacher.homework_done

advanced_python_teacher.check_homework(result_1)
temp_2 = Teacher.homework_done
assert temp_1 == temp_2

opp_teacher.check_homework(result_2)
opp_teacher.check_homework(result_3)

print(Teacher.homework_done[oop_hw])
Teacher.reset_results()
```
"""
from abc import ABC
from collections import defaultdict
from datetime import datetime, timedelta
from typing import Callable, TypeVar

DAYS_MESSAGE = "Must be > 0"
LATE_MESSAGE = "You are late"
NOT_HOMEWORK = "You gave a not Homework object"

StudentInstance = TypeVar("StudentInstance", bound=Callable)


class DeadlineError(Exception):
    """Raised when the homework is not active."""


class Document(ABC):  # pylint: disable=R0903 (too-few-public-methods)
    """
    Some document with exact date and time of creation.

    Attributes:
    -----------
    + `created` - date and time of homework creating.
    """

    def __init__(self):
        self.__created = datetime.now()

    @property
    def created(self) -> datetime:
        """Returns `created`."""
        return self.__created


class Person(ABC):
    """
    Takes `first_name` and `last_name` of the `Person`.

    Attributes:
    -----------
    + `first_name`
    + `last_name`
    """

    def __init__(self, first_name: str, last_name: str):
        self.__first_name = first_name
        self.__last_name = last_name

    @property
    def first_name(self) -> str:
        """Returns `first_name`."""
        return self.__first_name

    @property
    def last_name(self) -> str:
        """Returns `last_name`."""
        return self.__last_name


class Homework(Document):
    """
    Takes `text` and `deadline` of the `Homework`.

    Attributes:
    -----------
    + `text` - text of the homework task.
    + `deadline` - available number of days for task completing.
    If `deadline` <= 0 raises `ValueError("Must be > 0")`.
    + `created` - date and time of homework creating.

    Methods:
    --------
    + `is_active` - returns `True` if the deadline is ok, else `False`.
    """

    def __init__(self, text: str, deadline: int):
        super().__init__()
        self.__text = text
        self.__deadline = timedelta(days=self.__check(deadline))

    @property
    def text(self) -> str:
        """Returns `text`."""
        return self.__text

    @property
    def deadline(self) -> datetime:
        """Returns `deadline`."""
        return self.__deadline

    def is_active(self) -> bool:
        """
        Check `deadline` with (current time - `created`) and
        returns `True` if the deadline is ok, else `False`.
        """
        return self.deadline > datetime.now() - self.created

    @staticmethod
    def __check(days: int) -> int or None:
        """
        Returns `days` if `days` > 0, else
        raises `ValueError("Must be > 0")`.
        """
        if days > 0:
            return days
        raise ValueError(DAYS_MESSAGE)


class HomeworkResult(Document):
    """
    Takes `homework`, it's `solution` and `author`.

    Attributes:
    -----------
    + `author` - an instance of the `Student`.
    + `homework` - an instance of the `Homework`. If not it object is given,
    raises `TypeError("You gave a not Homework object")`.
    + `solution` - string with homework solution.
    + `created` - date and time of homework creating.
    """

    def __init__(self, author: StudentInstance, homework: Homework, solution: str):
        super().__init__()
        self.__author = author
        self.__homework = self.__check(homework)
        self.__solution = solution

    @property
    def author(self) -> StudentInstance:
        """Returns `autor`."""
        return self.__author

    @property
    def homework(self) -> Homework:
        """Returns `homework`."""
        return self.__homework

    @property
    def solution(self) -> str:
        """Returns `solution`."""
        return self.__solution

    @staticmethod
    def __check(homework: Homework) -> Homework or None:
        """
        Returns `homework` if it is an instance of the `Homework`,
        else raises `TypeError("You gave a not Homework object")`.
        """
        if isinstance(homework, Homework):
            return homework
        raise TypeError(NOT_HOMEWORK)


class Student(Person):
    """
    Takes `first_name` and `last_name` of the `Student`.

    Attributes:
    -----------
    + `first_name`
    + `last_name`

    Methods:
    --------
    + `do_homework` - takes `Homework` instance,
    returns `Homework` if the deadline is ok, else `None` and prints 'You are late'.
    """

    def do_homework(self, homework: Homework, solution: str) -> HomeworkResult or None:
        """
        Returns `Homework` if the deadline is ok,
        else raises `DeadlineError("You are late")`.
        """
        if homework.is_active():
            return HomeworkResult(
                homework=homework,
                solution=solution,
                author=self,
            )
        raise DeadlineError(LATE_MESSAGE)


class Teacher(Person):
    """
    Takes `first_name` and `last_name` of the `Teacher`.

    Attributes:
    -----------
    + `first_name`
    + `last_name`
    + `homework_done` - Class attribute.
    `defaultdict` with `{Homework: set(HomeworkResult)}` structure.

    Methods:
    --------
    + `create_homework` - takes `text` and `deadline`,
    returns `Homework` instance with `text` and `deadline`.
    + `check_homework` - takes `HomeworkResult`.
    + `reset_results` - takes `Homework` or `None`.
    """

    homework_done = defaultdict(set)

    @staticmethod
    def create_homework(text: str, deadline: int) -> Homework:
        """Returns `Homework` instance with `text` and `deadline`."""
        return Homework(text, deadline)

    def check_homework(self, homework_result: HomeworkResult) -> bool:
        """
        Returns `True` if `len(homework_result.solution)` > 5 and adds
        `homework_result` to the `homework_done` else returns `False`.
        """
        if len(homework_result.solution) > 5:
            self.homework_done[homework_result.homework].add(homework_result)
            return True
        return False

    @classmethod
    def reset_results(cls, homework: Homework = None):
        """
        Resets `homework` value to default in `homework_done`
        if `homework` is given else clears all `homework_done`.
        """
        if homework:
            del cls.homework_done[homework]
        else:
            cls.homework_done.clear()
