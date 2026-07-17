from typing import Literal

from pydantic import BaseModel, EmailStr

from app.models.user import UserRoleEnum


class CreateUserSchema(BaseModel):
    """Модель создания пользователя."""

    name: str
    email: EmailStr
    password: str
    age: int
    role: Literal[
        UserRoleEnum.ADMIN,
        UserRoleEnum.STUDENT,
        UserRoleEnum.TEACHER,
    ]


class UserSchema(CreateUserSchema):
    """Модель созданного пользователя."""

    id: int


class UserUpdateSchema(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    password: str | None = None
    age: int | None = None
    role: Literal[
        UserRoleEnum.ADMIN,
        UserRoleEnum.STUDENT,
        UserRoleEnum.TEACHER,
    ] | None
