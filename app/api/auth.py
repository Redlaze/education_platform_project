from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import select
from starlette import status
from starlette.responses import Response

from app.core.auth import get_password_hash, verify_password, create_access_token, get_current_user
from app.core.database import session_dep
from app.models import User
from app.schemas.user import CreateUserSchema, UserAuthSchema, UserSchema

router = APIRouter(prefix='/auth', tags=['Auth'])


@router.post('/register')
async def register_user(user_data: CreateUserSchema, session: session_dep):
    stmt = select(User).where(
        User.email == user_data.email,
    )
    find_user = await session.scalar(stmt)

    if find_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Такой пользователь уже существует',
        )

    user_dict = user_data.model_dump()
    user_dict['password'] = get_password_hash(user_data.password)

    new_user = User(**user_dict)
    session.add(new_user)

    await session.commit()
    await session.refresh(new_user)

    return {'message': 'Вы успешно зарегистрированы.'}


@router.post('/login')
async def login(response: Response, user_data: UserAuthSchema, session: session_dep):
    stmt = select(User).where(
        User.email == user_data.email,
    )
    find_user = await session.scalar(stmt)

    if not find_user or not verify_password(
        plain_password=user_data.password,
        hashed_password=find_user.password,
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Неверная почта или пароль',
        )

    access_token = create_access_token({'sub': str(find_user.id)})
    response.set_cookie(
        key='user_access_token',
        value=access_token,
        httponly=True,
    )

    return {'access_token': access_token, 'refresh_token': None}


@router.get('/me', response_model=UserSchema)
async def get_my_user_data(user: UserSchema = Depends(get_current_user)):
    return user


@router.post('/logout')
async def logout_user(response: Response):
    response.delete_cookie(key='user_access_token')
    return {'message': 'Вы вышли из системы.'}
