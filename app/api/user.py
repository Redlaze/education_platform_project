from fastapi import APIRouter, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from app.core.database import session_dep
from app.models import User
from app.schemas.user import CreateUserSchema, UserSchema, UserUpdateSchema

router = APIRouter(
    tags=['users'],
    prefix='/users',
)


@router.post('/create', response_model=UserSchema)
async def create_student(user: CreateUserSchema, session: session_dep):
    """Создает нового пользователя."""

    new_user = User(
        name=user.name,
        email=user.email,
        password=user.password,
        age=user.age,
    )
    session.add(new_user)
    try:
        await session.commit()
    except IntegrityError:
        raise HTTPException(status_code=400, detail='Такой пользователь уже существует')
    await session.refresh(new_user)

    return new_user


@router.get('/get', response_model=UserSchema)
async def get_user(email: str, session: session_dep):
    """Получает пользователя"""

    stmt = select(User).where(
        User.email == email,
    )
    user = await session.scalar(stmt)

    if not user:
        raise HTTPException(status_code=404, detail='Такого пользователя не существует!')

    return user


@router.patch('/update', response_model=UserSchema)
async def update_user(user_id: int, user_data: UserUpdateSchema, session: session_dep):
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
async def delete_user(user_id: int, session: session_dep):
    user = await session.get(User, user_id)

    if not user:
        raise HTTPException(status_code=404, detail='Такого пользователя не существует!')

    await session.delete(user)
    await session.commit()

    return {'status': 'success', 'deleted_user': user_id}
