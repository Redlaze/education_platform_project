import enum
from datetime import datetime

from typing_extensions import TYPE_CHECKING

from sqlalchemy import String, ForeignKey, Enum, Text, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models import Base


if TYPE_CHECKING:
    from app.models import User


class CourseStatusEnum(str, enum.Enum):
    DRAFT = 'draft'
    PUBLISHED = 'published'
    ARCHIVED = 'archived'


class Student(Base):
    __tablename__ = 'students'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    user: Mapped['User'] = relationship(
        'User',
        back_populates='courses',
    )
    course_id: Mapped[int] = mapped_column(ForeignKey('courses.id'))
    course: Mapped['Course'] = relationship(
        'Course',
        back_populates='students',
    )


class Course(Base):
    __tablename__ = 'courses'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(String(255))
    price: Mapped[float] = mapped_column(default=0.0)
    teacher_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=True)
    teacher: Mapped['User'] = relationship(
        'User',
        back_populates='teacher_course',
        uselist=False,
        lazy='joined',
    )
    students: Mapped[list['Student']] = relationship(
        'Student',
        back_populates='course',
        cascade="all, delete-orphan",
    )
    status: Mapped[CourseStatusEnum] = mapped_column(Enum(CourseStatusEnum), default=CourseStatusEnum.DRAFT)
    lessons: Mapped[list['Lesson']] = relationship(
        'Lesson',
        back_populates='course',
        cascade='all, delete-orphan',
        lazy='joined',
    )


class Lesson(Base):
    __tablename__ = 'lessons'

    id: Mapped[int] = mapped_column(primary_key=True)
    content: Mapped[Text] = mapped_column(Text, nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime, default=datetime.now)
    course_id: Mapped[int] = mapped_column(ForeignKey('courses.id'))
    course: Mapped['Course'] = relationship(
        'Course',
        back_populates='lessons',
        lazy='joined',
    )
    assignment: Mapped[Text] = mapped_column(Text, nullable=True)
    number: Mapped[int] = mapped_column(unique=True, nullable=False)
