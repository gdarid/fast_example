from typing import Sequence

from sqlalchemy import select
# from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.schema import User


class UserService:
    def __init__(self, session: AsyncSession):
        self._db = session

    async def list_users(self) -> Sequence[User]:
        result = await self._db.execute(select(User))
        return result.scalars().all()

    async def get_user(self, user_id: int) -> User | None:
        result = await self._db.execute(select(User).where(User.id == user_id))
        return result.scalars().first()

    async def check_name(self, name: str) -> bool:
        result = await self._db.execute(select(User).where(User.name == name))
        return result.scalars().first() is not None

    async def create_user(self, name: str) -> User:
        user = User(name=name)
        self._db.add(user)
        await self._db.commit()
        await self._db.refresh(user)
        return user

    async def update_user(self, user_id: int, name: str) -> User | None:
        user = await self.get_user(user_id)
        if not user:
            return None
        user.name = name
        await self._db.commit()
        await self._db.refresh(user)
        return user

    async def delete_user(self, user_id: int) -> bool:
        user = await self.get_user(user_id)
        if not user:
            return False
        await self._db.delete(user)
        await self._db.commit()
        return True
