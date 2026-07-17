import enum
from typing_extensions import TYPE_CHECKING

from sqlalchemy import String, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


if TYPE_CHECKING:
    from app.models import Course, Student


class UserRoleEnum(str, enum.Enum):
    STUDENT = 'student'
    ADMIN = 'admin'
    TEACHER = 'teacher'


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    email: Mapped[str] = mapped_column(String(255), unique=True)
    password: Mapped[str] = mapped_column(String(255))
    age: Mapped[int]
    role: Mapped[UserRoleEnum] = mapped_column(Enum(UserRoleEnum))
    teacher_course: Mapped["Course"] = relationship(
        'Course',
        back_populates='teacher',
        uselist=False,
    )
    courses: Mapped["Student"] = relationship(
        'Student',
        back_populates='user',
        cascade="all, delete-orphan",
    )
