"""
The main file which creates a final state of the `main.db`.
"""
import sys
from os import system

from sqlalchemy.ext.declarative import declarative_base

sys.path.append(".")
# pylint: disable=wrong-import-position

from homework_6.tasks.task_2 import Student, Teacher
from homework_12.task.models import HomeworkResultModel, ModelBase
from homework_12.task.sugars import session_manager, setup_session

DB = ModelBase
URL = "sqlite:///homework_12/main.db"


def generate_and_upgrade_migration(message: str):
    """
    Generates migration file with `message`
    at name and upgrades alembic head state.
    """
    system(f"alembic revision --message='{message}' --autogenerate")
    system("alembic upgrade head")


def create_models():
    """
    Generates schema migration file.
    """
    setup_session(URL, declarative_base())
    generate_and_upgrade_migration("create_models")


def write_records():
    """
    Writes some records.
    """
    with session_manager(URL, DB) as current:

        teacher = Teacher("Robert", "Drop")
        student = Student("Bobby", "Tables")

        task = teacher.create_homework("Task", 7)
        solution = student.do_homework(task, "Solution")

        current.add(HomeworkResultModel(solution, teacher))  # pylint: disable=no-member


if __name__ == "__main__":
    create_models()
    write_records()
