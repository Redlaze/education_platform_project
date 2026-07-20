from fastapi import APIRouter, HTTPException
from sqlalchemy import select
from starlette import status

from app.core.auth import current_user_dep
from app.core.database import session_dep
from app.models import User, Course
from app.schemas.course import CreateCourseSchema, CourseSchema
from app.schemas.user import UserSchema, UserUpdateSchema

router = APIRouter(
    tags=['admin'],
    prefix='/admin',
)


@router.patch('/users/update', response_model=UserSchema)
async def update_user(
    user_id: int,
    user_data: UserUpdateSchema,
    session: session_dep,
    current_user: current_user_dep,
):
    if current_user.role != 'admin':
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Не достаточно прав.'
        )


    user = await session.get(User, user_id)

    if not user:
        raise HTTPException(status_code=404, detail='Такого пользователя не существует!')

    updated_data = user_data.model_dump(exclude_unset=True)

    for user_key, user_value in updated_data.items():
        setattr(user, user_key, user_value)

    await session.commit()
    await session.refresh(user)

    return user


@router.delete('/users/delete')
async def delete_user(user_id: int, session: session_dep, current_user: current_user_dep):
    if current_user.role != 'admin':
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Не достаточно прав.'
        )

    user = await session.get(User, user_id)

    if not user:
        raise HTTPException(status_code=404, detail='Такого пользователя не существует!')

    await session.delete(user)
    await session.commit()

    return {'status': 'success', 'deleted_user': user_id}


@router.get('/users/', response_model=list[UserSchema])
async def get_all_users(session:session_dep, current_user: current_user_dep):
    if current_user.role != 'admin':
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Не достаточно прав.'
        )

    stmt = select(User)
    return await session.scalars(stmt)


@router.post('/courses', response_model=CourseSchema)
async def create_course(
    session: session_dep,
    course_data: CreateCourseSchema,
    current_user: current_user_dep
):
    if current_user.role not in ('admin', 'teacher'):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Не достаточно прав.'
        )

    teacher = await session.get(User, course_data.teacher_id)

    if not teacher or (teacher.role != 'teacher'):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Учителя с таким id не существует',
        )

    new_course = Course(
        name=course_data.name,
        description=course_data.description,
        status=course_data.status,
        price=course_data.price,
        teacher=teacher,
    )

    session.add(new_course)
    await session.commit()
    await session.refresh(new_course)

    return new_course
