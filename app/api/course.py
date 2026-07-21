from fastapi import APIRouter, HTTPException
from fastapi import Query
from sqlalchemy import select
from starlette import status

from app.core.auth import current_user_dep
from app.core.database import session_dep
from app.models import Course
from app.models.course import Lesson
from app.schemas.course import CourseSchema, LessonSchema, CreateLessonSchema

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


@router.get('/{id}', response_model=CourseSchema)
async def get_one_course(id: int, session: session_dep):
    course = await session.get(Course, id)

    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Не найден курс с таким ID',
        )

    return course


@router.post('/{id}/lessons', response_model=LessonSchema)
async def create_lesson(
    id: int, lesson_data: CreateLessonSchema,
    session: session_dep,
    current_user: current_user_dep,
):
    if current_user.role not in ('admin', 'teacher'):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Не достаточно прав.'
        )

    course = await session.get(Course, id)

    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Не найден курс с таким ID',
        )

    stmt = select(Lesson).where(
        Lesson.number==lesson_data.number,
    )
    lesson = await session.scalar(stmt)

    if lesson:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Урок с таким порядковым номером уже существует',
        )

    new_lesson = Lesson(
        content=lesson_data.content,
        course=course,
        assignment=lesson_data.assignment,
        number=lesson_data.number,
    )
    session.add(new_lesson)
    await session.commit()
    await session.refresh(new_lesson)

    return new_lesson
