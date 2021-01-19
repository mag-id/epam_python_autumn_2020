"""
Tests for `homework_12.task.models` using `homework_6.tasks.task_2`.
"""
from datetime import datetime
from typing import List, Tuple

import pytest
from sqlalchemy import select

from homework_6.tasks.task_2 import Student, Teacher
from homework_12.task.models import (
    HomeworkModel,
    HomeworkResultModel,
    ModelBase,
    StudentModel,
    TeacherModel,
)
from homework_12.task.sugars import session_manager

# https://stackoverflow.com/questions/10624937
TIME_FORMAT = "%Y-%m-%d %H:%M:%S.%f"


@pytest.fixture
def in_memory_session() -> "Session":
    """
    Yields `session` of the in-memory SQLite database.

    Note:
    -----
    Needs to be committed.
    """
    with session_manager("sqlite:///:memory:", ModelBase) as current:
        yield current


@pytest.fixture
def teacher() -> Teacher:
    """
    Returns `Teacher` instance. See `homework_6.task_2`.
    """
    return Teacher("Robert", "Drop")


@pytest.fixture
def student() -> Student:
    """
    Returns `Student` instance. See `homework_6.task_2`.
    """
    return Student("Bobby", "Tables")


def fetchall_result(session: "Session", model: ModelBase) -> List[Tuple]:
    """
    Returns `fetchall` result for current `session` and `model`.
    """
    return session.execute(select("*").select_from(model)).fetchall()


# https://stackoverflow.com/questions/18303924
def deadline_to_record(homework: "Homework") -> str:
    """
    Returns string with date and time of the
    `Homework.deadline` in formats of databases records.
    """
    return (datetime(1970, 1, 1) + homework.deadline).strftime(TIME_FORMAT)


# pylint: disable=redefined-outer-name


def test_teacher_model(in_memory_session, teacher):
    """
    Passes test if `TeacherModel` correctly recorded in the database.

    Format:
    -------
    (`teacher.first_name`: `str`, `teacher.second_name`: `str`, `id`: `int`)
    """
    in_memory_session.add(TeacherModel(teacher))
    in_memory_session.commit()

    result = fetchall_result(in_memory_session, TeacherModel)
    expected = [(teacher.first_name, teacher.last_name, 1)]

    assert result == expected


def test_student_model(in_memory_session, student):
    """
    Passes test if `StudentModel` correctly recorded in the database.

    Format:
    -------
    (`student.first_name`: `str`, `student.second_name`: `str`, `id`: `int`)
    """
    in_memory_session.add(StudentModel(student))
    in_memory_session.commit()

    result = fetchall_result(in_memory_session, StudentModel)
    expected = [(student.first_name, student.last_name, 1)]

    assert result == expected


def test_homework_model(in_memory_session, teacher):
    """
    Passes test if `HomeworkModel` correctly recorded in the database.

    Format:
    -------
    (
        `homework.created`: `TIME_FORMAT` `str`,
        `teacher_id`: `int`,
        `homework.text`: `str`,
        `homework.deadline`: `deadline_to_record` `str`,
        `id`: `int`
    )
    """
    homework = teacher.create_homework("Task", 7)

    in_memory_session.add(HomeworkModel(homework, teacher))
    in_memory_session.commit()

    result = fetchall_result(in_memory_session, HomeworkModel)
    expected = [
        (
            homework.created.strftime(TIME_FORMAT),
            1,
            homework.text,
            deadline_to_record(homework),
            1,
        )
    ]
    assert result == expected


def test_homework_result_model(in_memory_session, teacher, student):
    """
    Passes test if `HomeworkResultModel` correctly recorded in the database.

    Format:
    -------
    (
        `homework_result.created`: `TIME_FORMAT` `str`,
        `student_id`: `int`,
        `homework_result.solution`: `str`,
        `homework_id`: `int`,
        `id`: `int`
    )
    """
    homework = teacher.create_homework("Task", 7)
    homework_result = student.do_homework(homework, "Solution")

    record_homework_result = HomeworkResultModel(homework_result, teacher)

    in_memory_session.add(record_homework_result)
    in_memory_session.commit()

    result = fetchall_result(in_memory_session, HomeworkResultModel)
    expected = [
        (
            homework_result.created.strftime(TIME_FORMAT),
            1,
            homework_result.solution,
            1,
            1,
        )
    ]
    assert result == expected
