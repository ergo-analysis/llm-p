from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.schemas.auth import RegisterRequest, TokenResponse
from app.schemas.user import UserPublic
from app.usecases.auth import AuthUseCase
from app.core.errors import ConflictError, UnauthorizedError, NotFoundError

from app.api.deps import (
    get_auth_usecase,
    get_current_user_id,  
)
router = APIRouter(prefix="/auth", tags=["auth"])

AuthUseCaseDep = Annotated[AuthUseCase, Depends(get_auth_usecase)]
OAuthDep = Annotated[OAuth2PasswordRequestForm, Depends()]

@router.post("/register", response_model=UserPublic, status_code=status.HTTP_201_CREATED)
async def register(
    data: RegisterRequest,
    auth_usecase: AuthUseCaseDep,
) -> UserPublic:
    """Регистрация нового пользователя с email и паролем"""
    try:
        user = await auth_usecase.register(data)
        return user
    except ConflictError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))

@router.post("/login", response_model=TokenResponse)
async def login(
    data: OAuthDep,
    auth_usecase: AuthUseCaseDep
) -> TokenResponse:
    """Логин по email и паролю, возвращает JWT токен"""
    try:
        token_response = await auth_usecase.login(data.username, data.password)
        return token_response
    except UnauthorizedError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))

@router.get("/me", response_model=UserPublic)
async def get_me(
    auth_usecase: AuthUseCaseDep,
    user_id: int = Depends(get_current_user_id),
) -> UserPublic:
    """Возвращает публичную информацию текущего пользователя"""
    try:
        return await auth_usecase.get_profile(user_id)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
