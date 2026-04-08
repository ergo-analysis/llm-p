from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime 

class ChatRequest(BaseModel):
    """Запрос пользователя к LLM"""
    prompt: str = Field(..., description="Текст запроса")
    system: Optional[str] = Field(None, description="Системная инструкция")
    max_history: Optional[int] = Field(10, description="Длина истории контекста")
    temperature: Optional[float] = Field(0.7, ge=0.0, le=2.0, description="Креативность модели")

class ChatResponse(BaseModel):
    """Ответ LLM"""
    answer: str

class DialogMessage(BaseModel):
    """Сообщение как часть диалога"""
    role: str
    content: str
    created_at: datetime

    model_config = {"from_attributes": True}
