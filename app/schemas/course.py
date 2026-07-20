from typing import Literal

from pydantic import BaseModel

from app.models import CourseStatusEnum


class CreateCourseSchema(BaseModel):
    name: str
    description: str
    price: float
    status: Literal[
        CourseStatusEnum.DRAFT,
        CourseStatusEnum.ARCHIVED,
        CourseStatusEnum.PUBLISHED,
    ] = CourseStatusEnum.DRAFT


class CourseSchema(CreateCourseSchema):
    id: int
    teacher_id: int | None


class StudentSchema(BaseModel):
    id: int
    user_id: int
    course_id: int
