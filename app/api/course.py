from fastapi import APIRouter
from fastapi import Query
from sqlalchemy import select

from app.core.database import session_dep
from app.models import Course
from app.schemas.course import CourseSchema

router = APIRouter(prefix='/courses', tags=['courses'])


@router.get('/', response_model=list[CourseSchema])
async def get_all_courses(
    session: session_dep,
    size: int = Query(ge=1, le=100, default=10),
    page: int = Query(le=0, default=0)
):
    stmt = select(Course).limit(size).offset(page*size)
    courses = await session.scalars(stmt)

    return courses
