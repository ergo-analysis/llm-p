from app.core.security import _hash_password, _verify_password, create_access_token
from app.core.errors import ConflictError, UnauthorizedError, NotFoundError
from app.repositories.users import UserRepository
from app.schemas.auth import RegisterRequest, TokenResponse
from app.schemas.user import UserPublic
from app.db.models import User
 

class AuthUseCase:
    """Логика аутентификации"""
    def __init__(self, storage: UserRepository) -> None:
        self._storage = storage

    #подсмотрел у препода на лекции, удобно 
    def _public_response(self, data: User) -> UserPublic:
        return UserPublic.model_validate(data)

    async def register(self, data: RegisterRequest) -> UserPublic:
        """Регистрация"""
        occupied = await self._storage.get_by_email(data.email)
        if occupied:
            raise ConflictError("Этот email занят")

        hashed = _hash_password(data.password)
        user = await self._storage.create(data.email, hashed)
        return self._public_response(user)


    async def login(self, username: str, password: str) -> TokenResponse:
        """Логин и выдача токена"""
        user = await self._storage.get_by_email(username)
        if not user:
            raise UnauthorizedError("Неверный email или пароль")
        if not _verify_password(password, user.password_hash):
            raise UnauthorizedError("Неверный email или пароль")

        payload = {"sub": str(user.id), "role": user.role}
        token = create_access_token(payload)
        return TokenResponse(access_token=token)


    async def get_profile(self, user_id: int) -> UserPublic:
        """Возвращает публичную схему пользователя"""
        user = await self._storage.get_by_id(user_id)
        if not user:
            raise NotFoundError("Пользователь не найден")
        return self._public_response(user)
    