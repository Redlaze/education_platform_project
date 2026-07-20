from fastapi import APIRouter, HTTPException
from sqlalchemy import select
from starlette import status

from app.core.auth import current_user_dep
from app.core.database import session_dep
from app.models import User
from app.schemas.user import CreateUserSchema, UserSchema, UserUpdateSchema

router = APIRouter(
    tags=['users'],
    prefix='/users',
)


@router.post('/create', response_model=UserSchema)
async def create_user(user: CreateUserSchema, session: session_dep):
    """Создает нового пользователя."""


    stmt = select(User).where(
        User.email == user.email,
    )
    find_user = await session.scalar(stmt)

    if find_user:
        raise HTTPException(status_code=400, detail='Такой пользователь уже существует')

    new_user = User(
        name=user.name,
        email=user.email,
        password=user.password,
        age=user.age,
        role=user.role,
    )
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)

    return new_user


@router.get('/get', response_model=UserSchema)
async def get_user(email: str, session: session_dep, current_user: current_user_dep):
    """Получает пользователя"""

    if current_user.role != 'admin':
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Не достаточно прав.'
        )

    stmt = select(User).where(
        User.email == email,
    )
    user = await session.scalar(stmt)

    if not user:
        raise HTTPException(status_code=404, detail='Такого пользователя не существует!')

    return user


@router.patch('/update', response_model=UserSchema)
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


@router.delete('/delete')
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
