from pydantic import BaseModel, EmailStr

class UserPublic(BaseModel):
    """Публичная информация о пользователе"""
    id: int
    email: EmailStr
    role: str

    model_config = {"from_attributes": True}
