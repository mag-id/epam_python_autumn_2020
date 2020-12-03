"""
Unit tests for module `homework_5.tasks.task_1`.
"""
from datetime import datetime, timedelta
from unittest.mock import MagicMock

import pytest

from homework_5.tasks.task_1 import (
    DAYS_MESSAGE,
    LATE_MESSAGE,
    Homework,
    Student,
    Teacher,
)

FIXED_DAYS = datetime.now() - timedelta(days=2)


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
            pytest.param(-1, id="-1 raises ValueError(Must be > 0)"),
            pytest.param(0, id="0 raises ValueError(Must be > 0)"),
        ],
    )
    def test_negative_initialization(deadline):
        """
        Passes test if during `Homework` instance
        initialization raises `ValueError(DAYS_MESSAGE)`.
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
        monkeypatch.setattr("homework_5.tasks.task_1.Homework.created", FIXED_DAYS)
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
        monkeypatch.setattr("homework_5.tasks.task_1.Homework.created", FIXED_DAYS)
        assert Homework("some text", deadline).is_active()


class TestStudent:
    """Wraps tests for `Student`."""

    @staticmethod
    def test_do_homework_positive_returning():
        """Passes test if `do_homework(mock_homework)` returns `mock_homework`."""
        mock_homework = MagicMock(**{"is_active.return_value": True})
        assert (
            Student("Last name", "First name").do_homework(mock_homework)
            == mock_homework
        )

    @staticmethod
    def test_do_homework_negative_returning():
        """Passes test if `do_homework(mock_homework)` returns `None`."""
        mock_homework = MagicMock(**{"is_active.return_value": False})
        assert Student("Last name", "First name").do_homework(mock_homework) is None

    @staticmethod
    def test_do_homework_negative_side_effect(capsys):
        """Passes test if `do_homework(mock_homework)` prints `LATE_MESSAGE`."""
        mock_homework = MagicMock(**{"is_active.return_value": False})
        Student("Last name", "First name").do_homework(mock_homework)
        out, err = capsys.readouterr()
        assert (out, err) == (LATE_MESSAGE, "")


class TestTeacher:  # pylint: disable=R0903
    """Wraps tests for `Teacher`."""

    @staticmethod
    def test_create_homework():
        """Passes test if `create_homework("some task", 1)` is instance of `Homework`."""
        assert isinstance(
            Teacher("Last name", "First name").create_homework("some task", 1), Homework
        )
