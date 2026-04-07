from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from app.db.session import get_db
from app.repositories.users import UserRepository
from app.repositories.chat_messages import ChatMessageRepository
from app.services.openrouter_client import OpenRouterClient
from app.usecases.auth import AuthUseCase
from app.usecases.chat import ChatUseCase
from app.core.security import decode_access_token
from app.core.errors import UnauthorizedError

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

DbDep = Annotated[AsyncSession, Depends(get_db)]

async def get_openrouter_client() -> OpenRouterClient:
    return OpenRouterClient()

async def get_auth_usecase(db: DbDep) -> AuthUseCase:
    return AuthUseCase(UserRepository(db=db))

async def get_chat_usecase(
        db: DbDep, 
        llm_client: OpenRouterClient = Depends(get_openrouter_client)
        ) -> ChatUseCase:
    return ChatUseCase(ChatMessageRepository(db=db), llm_client=llm_client)

async def get_current_user_id(token: str = Depends(oauth2_scheme)) -> int:
    try:
        payload = decode_access_token(token)
        user_id = payload.get("sub")
        if user_id is None:
            raise UnauthorizedError("Неверный токен")
        return int(user_id)
    
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Недействительный токен",
            headers={"WWW-Authenticate": "Bearer"},
        )
