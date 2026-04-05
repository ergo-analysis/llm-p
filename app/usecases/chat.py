from app.repositories.chat_messages import ChatMessageRepository
from app.services.openrouter_client import OpenRouterClient
from app.schemas.chat import ChatResponse, ChatRequest, DialogMessage


class ChatUseCase:
    def __init__(self, storage: ChatMessageRepository, llm_client: OpenRouterClient) -> None:
        self.storage = storage
        self.llm_client = llm_client

    async def ask(self, user_id: int, data: ChatRequest) -> ChatResponse:

        messages = []

        if data.system:
            messages.append({"role": "system", "content": data.system})

        history = await self.storage.get_last_messages(user_id, limit=data.max_history)
        for message in history:
            messages.append({"role": message.role, "content": message.content})

        messages.append({"role": "user", "content": data.prompt})

        await self.storage.add_message(user_id, "user", data.prompt)

        answer = await self.llm_client.chat_completion(messages, temperature=data.temperature)

        await self.storage.add_message(user_id, "assistant", answer)

        return ChatResponse(answer)

    async def get_history(self, user_id: int, limit: int | None = None) -> list[DialogMessage]:
        messages = await self.storage.get_last_messages(user_id, limit=limit)
        dialog = [DialogMessage.model_validate(message) for message in messages]

        return dialog #мб добавить реверс списка, чтоб читать от поздних к ранним?

    async def clear_history(self, user_id: int) -> None:
        await self.storage.delete_user_history(user_id)

