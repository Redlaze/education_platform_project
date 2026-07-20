from typing import Annotated

from fastapi import Depends
from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone

from starlette import status
from starlette.exceptions import HTTPException
from starlette.requests import Request

from app.core.config import get_auth_data
from app.core.database import session_dep
from app.models import User
from app.schemas.user import UserSchema

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def get_password_hash(password: str) -> str:
    """Хэширует переданный пароль

    Args:
        password: переданный пароль.
    Returns:
        Хэшированный пароль.
    """

    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Проверяет правильность введенного пароля.

    Args:
        plain_password: введенный пароль;
        hashed_password: существующий хэшированный пароль.

    Returns:
        Указывает правильно или неправильно введен пароль.
    """

    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict) -> str:
    """Создает JWT-токен.

    Args:
        данные для создания токена.

    Returns:
        JWT-токен.
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=30)
    to_encode.update({'exp': expire})
    auth_data = get_auth_data()
    encode_jwt = jwt.encode(
        to_encode,
        auth_data['secret_key'],
        algorithm=auth_data['algorithm']
    )

    return encode_jwt


def get_token(request: Request):
    token = request.cookies.get('user_access_token')

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Вы не авторизованы',
        )

    return token


def get_user_id(token: str = Depends(get_token)):
    try:
        auth_data = get_auth_data()
        payload = jwt.decode(
            token=token,
            key=auth_data['secret_key'],
            algorithms=[auth_data['algorithm']],
        )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Токен не валидный',
        )

    expire = payload.get('exp')

    if not expire:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Токен истек',
        )

    expire_time = datetime.fromtimestamp(int(expire), tz=timezone.utc)

    if expire_time < datetime.now(timezone.utc):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Токен истек',
        )

    user_id = payload.get('sub')

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Не найден ID пользователя',
        )

    return int(user_id)


async def get_current_user(session: session_dep, user_id: int = Depends(get_user_id)):
    user = await session.get(User, user_id)
    return user


current_user_dep = Annotated[UserSchema, Depends(get_current_user)]