from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import ChatMessage

class ChatMessageRepository:
    """Репозиторий сообщений чата"""
    def __init__(self, db: AsyncSession):
        self._db = db

    async def add_message(self, user_id: int, role: str, content: str) -> ChatMessage:
        """Добавляет сообщения в историю"""
        message = ChatMessage(
            user_id=user_id,
            role=role,
            content=content,
        )
        self._db.add(message)
        await self._db.commit()
        await self._db.refresh(message)
        return message


    async def get_last_messages(self, user_id: int, limit: int | None = 10 ) -> list[ChatMessage]:
        """Получает последние limit сообщений"""
        result = await self._db.scalars(
            select(ChatMessage)
            .where(ChatMessage.user_id == user_id)
            .order_by(ChatMessage.created_at.desc())
            .limit(limit))
            
        messages = result.all()

        return messages[::-1] #тут надо развернуть, будет от последнего-9 до последнего


    async def delete_user_history(self, user_id: int) -> None:
        """Удаляет историю пользователя"""
        await self._db.execute(
            delete(ChatMessage)
            .where(ChatMessage.user_id == user_id))
        
        await self._db.commit()
        