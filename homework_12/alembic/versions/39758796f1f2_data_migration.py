# pylint: disable=wrong-import-position, import-error, invalid-name
"""data_migration

Revision ID: 39758796f1f2
Revises: ae2843fc10ff
Create Date: 2021-01-19 03:53:18.635806

"""
import sys

sys.path.append(".")

from homework_6.tasks.task_2 import Student, Teacher
from homework_12.task.main import DB, URL
from homework_12.task.models import (
    HomeworkModel,
    HomeworkResultModel,
    StudentModel,
    TeacherModel,
)
from homework_12.task.sugars import session_manager

# revision identifiers, used by Alembic.
revision = "39758796f1f2"
down_revision = "ae2843fc10ff"
branch_labels = None
depends_on = None


def upgrade():
    """
    Writes some records.
    """
    with session_manager(URL, DB) as current:

        teacher = Teacher("Robert", "Drop")
        student = Student("Bobby", "Tables")

        task = teacher.create_homework("Task", 7)
        solution = student.do_homework(task, "Solution")

        current.add(HomeworkResultModel(solution, teacher))  # pylint: disable=no-member


def downgrade():
    """
    Cleans all `HomeworkResultModel`,
    `HomeworkModel`, `StudentModel`,
    `TeacherModel` records.
    """
    with session_manager(URL, DB) as current:
        # pylint: disable=no-member
        current.query(HomeworkResultModel).delete()
        current.query(HomeworkModel).delete()
        current.query(StudentModel).delete()
        current.query(TeacherModel).delete()
