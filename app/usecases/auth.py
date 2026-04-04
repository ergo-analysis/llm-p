from app.core.security import _hash_password, _verify_password, create_access_token
from app.core.errors import ConflictError, UnauthorizedError, NotFoundError
from app.repositories.users import UserRepository
from app.schemas.auth import RegisterRequest, LoginRequest, TokenResponse
from app.schemas.user import UserPublic
 

class AuthUsecase:
    def __init__(self, storage: UserRepository):
        self._storage = storage


    async def register(self, data: RegisterRequest) -> UserPublic:

        occupied = await self._storage.get_by_email(data.email)
        if occupied:
            raise ConflictError("Этот email занят")

        hashed = _hash_password(data.password)
        user = await self._storage.create(data.email, hashed)
        return user


    async def login(self, data: LoginRequest) -> TokenResponse:

        user = await self._storage.get_by_email(data.username)
        if not user:
            raise UnauthorizedError("Неверный email или пароль")
        if not _verify_password(data.password, user.password_hash):
            raise UnauthorizedError("Неверный email или пароль")

        payload = {"sub": str(user.id), "role": user.role}
        token = create_access_token(payload)
        return TokenResponse(access_token=token)


    async def get_profile(self, user_id: int) -> UserPublic:

        user = await self._storage.get_by_id(user_id)
        if not user:
            raise NotFoundError("Пользователь не найден")
        return user
    