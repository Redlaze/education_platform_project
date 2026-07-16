from typing import Optional

from pydantic import BaseModel, EmailStr


class CreateUserSchema(BaseModel):
    """Модель создания пользователя."""

    name: str
    email: EmailStr
    password: str
    age: int


class UserSchema(CreateUserSchema):
    """Модель созданного пользователя."""

    id: int


class UserUpdateSchema(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    password: str | None = None
    age: int | None = None
