"""
SQLAlchemy `ModelBase` class with related models:
+ `DocumentModel`
+ `PersonModel`
+ `StudentModel`
+ `TeacherModel`
+ `HomeworkModel`
+ `HomeworkResultModel`
"""

from sqlalchemy import Column, DateTime, ForeignKey, Integer, Interval, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

# pylint: disable=too-few-public-methods

__all__ = [
    "ModelBase",
    "StudentModel",
    "TeacherModel",
    "HomeworkModel",
    "HomeworkResultModel",
]

ModelBase = declarative_base()


class DocumentModel(ModelBase):
    """
    SQLAlchemy abstract model for `Document` from `homework_6.task_2`.

    Takes `document` and records `Document.created` as `DateTime`.
    """

    __abstract__ = True

    created = Column(DateTime, nullable=False)

    def __init__(self, document: "Document"):
        self.created = document.created


class PersonModel(ModelBase):
    """
    SQLAlchemy abstract model for `Person` from `homework_6.task_2`.

    Takes `person` and records `Person.first_name` with `Person.last_name` as `String`s.
    """

    __abstract__ = True

    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)

    def __init__(self, person: "Person"):
        self.first_name = person.first_name
        self.last_name = person.last_name


class StudentModel(PersonModel):
    """
    SQLAlchemy model for `Student` from `homework_6.task_2`.

    Takes `document` and records `Document.created`
    as `DateTime` into `"student"` table.

    `StudentModel.result` related with `HomeworkResultModel.student`
    as one-to-many.
    """

    __tablename__ = "student"

    id = Column(Integer, primary_key=True)

    result = relationship("HomeworkResultModel", back_populates="student")


class TeacherModel(PersonModel):
    """
    SQLAlchemy model for `Teacher` from `homework_6.task_2`.

    Takes `person` and records `Person.first_name` with
    `Person.last_name` as `String`s into `"teacher"` table.

    `TeacherModel.homework` related with `HomeworkModel.teacher`
    as one-to-many.
    """

    __tablename__ = "teacher"

    id = Column(Integer, primary_key=True)

    homework = relationship("HomeworkModel", back_populates="teacher")


class HomeworkModel(DocumentModel):
    """
    SQLAlchemy model for `Homework` from `homework_6.task_2`.

    Takes `homework_` and records `Homework.text` as `String`,
    `Homework.deadline` as `Interval` into `"teacher"` table.

    Also takes `teacher_` for relationships configuring.

    `TeacherModel.homework` related with `HomeworkModel.teacher`
    as one-to-many.

    `HomeworkModel.result` related with `HomeworkResultModel.homework`
    as one-to-many.
    """

    __tablename__ = "homework"

    id = Column(Integer, primary_key=True)

    text = Column(String, nullable=False)
    deadline = Column(Interval, nullable=False)

    teacher_id = Column(Integer, ForeignKey("teacher.id"))
    teacher = relationship(TeacherModel, back_populates="homework")

    result = relationship("HomeworkResultModel", back_populates="homework")

    def __init__(self, homework_: "Homework", teacher_: "Teacher"):
        super().__init__(homework_)
        self.text = homework_.text
        self.deadline = homework_.deadline
        self.teacher = TeacherModel(teacher_)


class HomeworkResultModel(DocumentModel):
    """
    SQLAlchemy model for `HomeworkResult` from `homework_6.task_2`.

    Takes `homework_result_` and records `HomeworkResult.solution`
    as `String` into `"teacher"` table.

    Also takes `teacher_` for relationships configuring.

    `StudentModel.result` related with `HomeworkResultModel.student`
    as one-to-many.

    `HomeworkModel.result` related with `HomeworkResultModel.homework`
    as one-to-many.
    """

    __tablename__ = "result"
    id = Column(Integer, primary_key=True)

    solution = Column(String, nullable=False)

    student_id = Column(Integer, ForeignKey("student.id"))
    student = relationship(StudentModel, back_populates="result")

    homework_id = Column(Integer, ForeignKey("homework.id"))
    homework = relationship(HomeworkModel, back_populates="result")

    def __init__(self, homework_result_: "HomeworkResult", teacher_: "Teacher"):
        super().__init__(homework_result_)
        self.solution = homework_result_.solution
        self.homework = HomeworkModel(homework_result_.homework, teacher_)
        self.student = StudentModel(homework_result_.author)
