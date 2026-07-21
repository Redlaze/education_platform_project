from pydantic import BaseModel, EmailStr


class TeacherSchema(BaseModel):
    """Модель учителя."""

    id: int
    name: str
    email: EmailStr
    age: int
