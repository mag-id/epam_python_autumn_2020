"""
Unit tests for module `homework_6.tasks.task_2`.
"""

from collections import defaultdict
from datetime import datetime, timedelta
from unittest.mock import MagicMock

import pytest

from homework_6.tasks.task_2 import (
    DAYS_MESSAGE,
    LATE_MESSAGE,
    NOT_HOMEWORK,
    DeadlineError,
    Homework,
    HomeworkResult,
    Student,
    Teacher,
)

FIXED_DAYS = datetime.now() - timedelta(days=2)
PATHCED_CREATED = "homework_6.tasks.task_2.Homework.created"
PATCHED_IS_ACTIVE = "is_active.return_value"
PATCHED_HOMEWORK_DONE = "homework_6.tasks.task_2.Teacher.homework_done"


class TestHomework:
    """Wraps tests for `Homework`."""

    @staticmethod
    def test_positive_initialization():
        """
        Passes test if `Homework(text="some task", deadline=1)`
        instance is initialize properly.
        """
        homework = Homework(text="some task", deadline=1)
        assert isinstance(homework.text, str)
        assert isinstance(homework.deadline, timedelta)
        assert isinstance(homework.created, datetime)

    @staticmethod
    @pytest.mark.parametrize(
        ["deadline"],
        [
            pytest.param(-1, id="deadline = -1 raises ValueError(DAYS_MESSAGE)"),
            pytest.param(0, id="deadline = -1 raises ValueError(DAYS_MESSAGE)"),
        ],
    )
    def test_negative_initialization(deadline: int):
        """
        Passes test if during `Homework` instance
        initialization `ValueError` with `DAYS_MESSAGE` occurs.
        """
        with pytest.raises(ValueError, match=DAYS_MESSAGE):
            Homework(text="some task", deadline=deadline)

    @staticmethod
    @pytest.mark.parametrize(
        ["deadline"],
        [
            pytest.param(1, id="False: the deadline was yesterday."),
            pytest.param(2, id="False: today is the deadline."),
        ],
    )
    def test_is_active_false(monkeypatch, deadline: int):
        """Passes test if `is_active` returns `False`."""
        monkeypatch.setattr(PATHCED_CREATED, FIXED_DAYS)
        assert Homework("some text", deadline).is_active() is False

    @staticmethod
    @pytest.mark.parametrize(
        ["deadline"],
        [
            pytest.param(3, id="True: deadline will be tomorrow."),
            pytest.param(4, id="True: deadline will be after tomorrow."),
        ],
    )
    def test_is_active_true(monkeypatch, deadline: int):
        """Passes test if `is_active` returns `True`."""
        monkeypatch.setattr(PATHCED_CREATED, FIXED_DAYS)
        assert Homework("some text", deadline).is_active()


class TestHomeworkResult:
    """Wraps tests for `Homework`."""

    @staticmethod
    def test_positive_initialization():
        """
        Passes test if `HomeworkResult` instance is initialize properly.
        """
        homework_result = HomeworkResult(
            homework=Homework("some task", 1),
            solution="some solution",
            author=Student("First name", "Last name"),
        )
        assert isinstance(homework_result.homework, Homework)
        assert isinstance(homework_result.solution, str)
        assert isinstance(homework_result.author, Student)
        assert isinstance(homework_result.created, datetime)

    @staticmethod
    def test_student_type_error():
        """
        Passes test if `HomeworkResult` with wrong `homework`
        attribute raises `TypeError(NOT_HOMEWORK)` exception.
        """
        with pytest.raises(TypeError, match=NOT_HOMEWORK):
            HomeworkResult(
                homework="not homework instance",
                solution="some solution",
                author=Student("First name", "Last name"),
            )


class TestStudent:
    """Wraps tests for `Student`."""

    @staticmethod
    def test_do_homework_positive_returning():
        """
        Passes test if `do_homework` returns
        correct `HomeworkResult` instance.
        """
        student = Student("First name", "Last name")
        homework = Homework("some task", 1)
        solution = "some solution"

        homework_result = student.do_homework(homework, solution)

        assert isinstance(homework_result, HomeworkResult)
        assert homework_result.homework is homework
        assert homework_result.author is student
        assert homework_result.solution == solution

    @staticmethod
    def test_do_homework_negative_returning():
        """
        Passes test if `do_homework` raises
        `DeadlineError(LATE_MESSAGE)` exception.
        """
        with pytest.raises(DeadlineError, match=LATE_MESSAGE):
            mock_homework = MagicMock(**{PATCHED_IS_ACTIVE: False})
            student = Student("First name", "Last name")
            student.do_homework(mock_homework, "some solution")


class TestTeacher:
    """Wraps tests for `Teacher`."""

    @staticmethod
    def test_create_homework():
        """
        Passes test if `create_homework` returns the instance of `Homework`.
        """
        teacher = Teacher("First name", "Last name")
        assert isinstance(teacher.create_homework("some task", 1), Homework)

    @staticmethod
    def test_reset_results(monkeypatch):
        """
        Passes test if `reset_results(homework)`
        deletes `homework` key-value pair, and
        `reset_results()` clears all `homework_done`.
        """
        monkeypatch.setattr(PATCHED_HOMEWORK_DONE, defaultdict(set))

        first_key, first_value = "first_key", "first_value"
        second_key, second_value = "second_key", "second_value"

        Teacher.homework_done[first_key].add(first_value)
        Teacher.homework_done[second_key].add(second_value)

        Teacher.reset_results(second_key)
        assert len(Teacher.homework_done) == 1
        assert first_key in Teacher.homework_done

        Teacher.reset_results()
        assert len(Teacher.homework_done) == 0

    class TestCheckHomework:
        """Wraps tests for `check_homework`."""

        @staticmethod
        @pytest.mark.parametrize(
            ["solution", "expected_result"],
            [
                pytest.param("More than 6", True, id="len(solution) = 11"),
                pytest.param("123456", True, id="len(solution) = 6"),
                pytest.param("12345", False, id="len(solution) = 5"),
                pytest.param("Les5", False, id="len(solution) = 4"),
            ],
        )
        def test_returning(monkeypatch, solution: str, expected_result: bool):
            """
            Passes test if `check_homework` returns `True` for `solution`
            if `len(solution)` > 5 or `False` if `len(solution)` <= 5.
            """
            monkeypatch.setattr(PATCHED_HOMEWORK_DONE, defaultdict(set))
            mock_homework_result = MagicMock(solution=solution)

            teacher = Teacher("First name", "Last name")
            assert teacher.check_homework(mock_homework_result) is expected_result

        @staticmethod
        @pytest.mark.parametrize(
            ["solution", "expected_result"],
            [
                pytest.param("More than 6", True, id="len(solution) = 11"),
                pytest.param("123456", True, id="len(solution) = 6"),
                pytest.param("12345", False, id="len(solution) = 5"),
                pytest.param("Les5", False, id="len(solution) = 4"),
            ],
        )
        def test_side_effects(monkeypatch, solution: str, expected_result: bool):
            """
            Passes test if `check_homework` update `Teacher.homework_done` (`True`)
            if `len(solution)` > 5 or do not update if `len(solution)` <= 5 (`False`).
            """
            mock_homework_done = defaultdict(set)
            monkeypatch.setattr(PATCHED_HOMEWORK_DONE, mock_homework_done)

            teacher = Teacher("First name", "Last name")
            homework = "homework instance"
            mock_homework_result = MagicMock(
                homework=homework,
                solution=solution,
            )
            teacher.check_homework(mock_homework_result)

            reference = defaultdict(set, {homework: {mock_homework_result}})

            assert (mock_homework_done == reference) is expected_result
