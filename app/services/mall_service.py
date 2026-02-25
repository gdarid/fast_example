from typing import Sequence

# from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from app.db.schema import Mall, Account


class MallService:
    def __init__(self, session: AsyncSession):
        self._db = session

    async def check_commit(self) -> bool:
        try:
            await self._db.commit()
        except IntegrityError:
            await self._db.rollback()
            return False

        return True

    async def list_malls(self) -> Sequence[Mall]:
        result = await self._db.execute(select(Mall))
        return result.scalars().all()

    async def get_mall(self, mall_id: int) -> Mall | None:
        result = await self._db.execute(select(Mall).where(Mall.id == mall_id))
        return result.scalars().first()

    async def check_name(self, name: str) -> bool:
        result = await self._db.execute(select(Mall).where(Mall.name == name))
        return result.scalars().first() is not None

    async def create_mall(self, name: str, owner_id: int) -> Mall | None:
        result = await self._db.execute(select(Account).where(Account.id == owner_id))
        account = result.scalars().first()
        if not account:
            return None
        mall = Mall(name=name, owner_id=owner_id)
        self._db.add(mall)

        if not await self.check_commit():
            return None

        await self._db.refresh(mall)
        return mall

    async def update_mall(self, mall_id: int, name: str, owner_id: int | None) -> Mall | None:
        mall = await self.get_mall(mall_id)
        if not mall:
            return None
        if owner_id is not None:
            result = await self._db.execute(select(Account).where(Account.id == owner_id))
            account = result.scalars().first()
            if not account:
                return None
            mall.owner_id = owner_id
        mall.name = name

        if not await self.check_commit():
            return None

        await self._db.refresh(mall)
        return mall

    async def delete_mall(self, mall_id: int) -> bool:
        mall = await self.get_mall(mall_id)
        if not mall:
            return False
        await self._db.delete(mall)
        await self._db.commit()
        return True
