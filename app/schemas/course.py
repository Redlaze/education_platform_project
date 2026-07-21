from typing import Literal

from pydantic import BaseModel

from app.models import CourseStatusEnum
from app.schemas.teacher import TeacherSchema
from app.schemas.user import UserSchema


class CreateCourseSchema(BaseModel):
    name: str
    description: str
    price: float
    status: Literal[
        CourseStatusEnum.DRAFT,
        CourseStatusEnum.ARCHIVED,
        CourseStatusEnum.PUBLISHED,
    ] = CourseStatusEnum.DRAFT
    teacher_id: int


class CourseSchema(CreateCourseSchema):
    id: int
    teacher: TeacherSchema


class StudentSchema(BaseModel):
    id: int
    user: UserSchema
    course: CourseSchema


class CreateLessonSchema(BaseModel):
    name: str
    content: str
    assignment: str
    number: int


class LessonSchema(CreateLessonSchema):
    id: int
    course: CourseSchema


class StudentLessonCompleteSchema(BaseModel):
    id: int
    student: UserSchema
    lesson: LessonSchema
    is_completed: bool
