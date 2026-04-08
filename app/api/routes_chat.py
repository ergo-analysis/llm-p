from typing import Annotated, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from app.schemas.chat import ChatRequest, ChatResponse, DialogMessage
from app.usecases.chat import ChatUseCase
from app.api.deps import get_chat_usecase, get_current_user_id
from app.core.errors import ExternalServiceError

router = APIRouter(prefix="/chat", tags=["chat"])

ChatUseCaseDep = Annotated[ChatUseCase, Depends(get_chat_usecase)]
UserIdDep = Annotated[int, Depends(get_current_user_id)]

@router.post("/", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    user_id: UserIdDep,
    chat_usecase: ChatUseCaseDep,
) -> ChatResponse:
    """
    Отправляет запрос к LLM.
    Возвращает ответ.
    Сохраняет историю в бд.
    """
    try:
        response = await chat_usecase.ask(user_id, request)
        return response
    except ExternalServiceError as e:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=str(e))

@router.get("/history", response_model=list[DialogMessage])
async def get_history(
    user_id: UserIdDep,
    chat_usecase: ChatUseCaseDep,
    limit: Optional[int] = Query(10, description="Количество последних сообщений"),
    ) -> list[DialogMessage]:
    """Возвращает последние limit сообщений диалога"""

    messages = await chat_usecase.get_history(user_id, limit)
    return messages

@router.delete("/history", status_code=status.HTTP_204_NO_CONTENT)
async def clear_history(
    user_id: UserIdDep,
    chat_usecase: ChatUseCaseDep,
    ):
    """Удаляет историю диалога"""
    await chat_usecase.clear_history(user_id)
    return None
