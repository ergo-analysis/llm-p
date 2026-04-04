from pydantic import BaseModel, EmailStr, Field
from enum import StrEnum

class UserRole(StrEnum):
    ADMIN = 'admin'
    USER = 'user'

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6, description="Пароль не менее 6 символов")

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class LoginRequest(BaseModel):
    username: str
    password: str

class AuthUser(BaseModel):
    username: str
    role: UserRole
