from app.repositories.chat_messages import ChatMessageRepository
from app.services.openrouter_client import OpenRouterClient

class ChatUseCase:
    def __init__(self, message_repo: ChatMessageRepository, llm_client: OpenRouterClient):
        self.message_repo = message_repo
        self.llm_client = llm_client

    async def ask(
        self,
        user_id: int,
        prompt: str,
        system: str | None = None,
        max_history: int = 10,
        temperature: float = 0.7
    ) -> str:

        messages = []

        if system:
            messages.append({"role": "system", "content": system})

        history = await self.message_repo.get_last_messages(user_id, limit=max_history)
        for message in history:
            messages.append({"role": message.role, "content": message.content})

        messages.append({"role": "user", "content": prompt})

        await self.message_repo.add_message(user_id, "user", prompt)

        answer = await self.llm_client.chat_completion(messages, temperature=temperature)

        await self.message_repo.add_message(user_id, "assistant", answer)

        return answer

    async def get_history(self, user_id: int, limit: int = 50) -> list[dict]:
        messages = await self.message_repo.get_last_messages(user_id, limit=limit)
        return [{"role": m.role, "content": m.content, "created_at": m.created_at.isoformat()} for m in messages]

    async def clear_history(self, user_id: int) -> None:
        await self.message_repo.delete_user_history(user_id)

