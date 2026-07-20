from typing import Literal

from pydantic import BaseModel

from app.models import CourseStatusEnum
from app.schemas.teacher import TeacherSchema


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
    user_id: int
    course_id: int
