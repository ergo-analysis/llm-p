from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime 

class ChatRequest(BaseModel):
    prompt: str = Field(..., description="Текст запроса")
    system: Optional[str] = Field(None, description="Системная инструкция")
    max_history: Optional[int] = Field(10, description="Длина истории контекста")
    temperature: Optional[float] = Field(0.7, ge=0.0, le=2.0, description="Креативность модели")

class ChatResponse(BaseModel):
    answer: str

class DialogMessage(BaseModel):
    role: str
    content: str
    created_at: datetime

    model_config = {"from_attributes": True}

