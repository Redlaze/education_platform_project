from pydantic import BaseModel, EmailStr


class TeacherSchema(BaseModel):
    """Модель учителя."""

    name: str
    email: EmailStr
    age: int
