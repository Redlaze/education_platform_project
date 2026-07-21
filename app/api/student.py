from fastapi import APIRouter, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from starlette import status

from app.core.auth import current_user_dep
from app.core.database import session_dep
from app.models import Student, Course, Lesson
from app.models.course import StudentLessonComplete
from app.schemas.course import StudentSchema, LessonSchema

router = APIRouter(prefix='/student', tags=['students'])


@router.post('/courses/{course_id}/enroll', response_model=StudentSchema)
async def enroll_course(course_id: int, session: session_dep, current_user: current_user_dep):
    course = await session.get(Course, course_id)

    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Не найден курс с таким ID',
        )

    stmt = select(Student).where(
        Student.user_id==current_user.id,
    )

    if await session.scalar(stmt):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Вы уже записаны на этот курс',
        )

    new_student = Student(
        user=current_user,
        course=course,
    )
    session.add(new_student)
    await session.commit()
    await session.refresh(new_student)

    return new_student


@router.get('/my_courses', response_model=list[StudentSchema])
async def get_my_all_courses(session: session_dep, current_user: current_user_dep):
    stmt = select(Student).where(
        Student.user_id == current_user.id,
    )
    courses = await session.scalars(stmt)

    return courses


@router.get('/course/{course_id}/lessons', response_model=list[LessonSchema])
async def get_my_course_lessons(course_id: int, session: session_dep, current_user: current_user_dep):
    student_query = await session.execute(
        select(Student)
        .where(
            Student.user_id == current_user.id,
            Student.course_id == course_id,
        )
        .options(
            joinedload(Student.course)
            .joinedload(Course.lessons),
        )
    )
    student = student_query.unique().scalar_one()

    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Вы не записаны на курс "{student.course.name}"'
        )

    return student.course.lessons


@router.post('/lesson/{lesson_id}/complete')
async def complete_lesson(lesson_id: int, session: session_dep, current_user: current_user_dep):
    lesson = await session.get(Lesson, lesson_id)

    if not lesson:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Урок с данным ID не существует.'
        )

    student_stmt = select(Student).where(
        Student.user_id == current_user.id,
    )
    student = await session.scalar(student_stmt)

    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Вы не записаны на курс "{lesson.course.name}"'
        )

    find_completed_lesson_stmt = select(StudentLessonComplete).where(
        StudentLessonComplete.student_id == student.id,
    )

    find_completed_lesson = await session.scalar(find_completed_lesson_stmt)

    if find_completed_lesson:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f'Вы уже прошли урок "{lesson.name}"'
        )

    completed_lesson = StudentLessonComplete(
        student=student,
        lesson=lesson,
        is_completed=True,
    )
    session.add(completed_lesson)
    await session.commit()
    await session.refresh(completed_lesson)

    return {'message': f'Урок "{lesson.name}" пройден'}
