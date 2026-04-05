from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.models import User

class UserRepository:
    def __init__(self, db: AsyncSession):
        self._db = db

    """def _to_response(self, user: User) -> UserPublic:
        return UserPublic(
            id=user.id,
            email=user.email,
            role=user.role
        )
        """ #мб лишнее

    async def get_by_id(self, user_id: int) -> User | None:
        user = await self._db.get(User, user_id)
        #if user is None: проверка мб избыточна
        #    return None 
        return user #self._to_response(user)

    async def get_by_email(self, user_email: str) -> User | None:
        user = await self._db.scalar(select(User).where(User.email == user_email)) 
        #if user is None:
        #    return None
        return user #self._to_response(user)

    async def create(self, email, password_hash) -> User:
        user = User(
            email=email,
            password_hash=password_hash,
        )
        self._db.add(user)
        await self._db.commit()
        await self._db.refresh(user)
        added_user = await self.get_by_email(email)
        return added_user
