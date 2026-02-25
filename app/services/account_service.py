from typing import Sequence

from sqlalchemy import select
# from sqlalchemy.orm import Session
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from app.db.schema import Account, Mall


class AccountService:
    def __init__(self, session: AsyncSession):
        self._db = session

    async def check_commit(self) -> bool:
        try:
            await self._db.commit()
        except IntegrityError:
            await self._db.rollback()
            return False

        return True

    async def list_accounts(self) -> Sequence[Account]:
        result = await self._db.execute(
            select(Account).options(selectinload(Account.malls))
        )
        return result.scalars().all()

    async def get_account(self, account_id: int) -> Account | None:
        result = await self._db.execute(
            select(Account)
            .options(selectinload(Account.malls))
            .where(Account.id == account_id)
        )
        return result.scalars().first()

    async def check_name(self, name: str) -> bool:
        result = await self._db.execute(select(Account).where(Account.name == name))
        return result.scalars().first() is not None

    async def create_account(self, name: str) -> Account | None:
        account = Account(name=name)
        self._db.add(account)
        if not await self.check_commit():
            return None
        await self._db.refresh(account)
        return account

    async def update_account(self, account_id: int, name: str) -> Account | None:
        account = await self.get_account(account_id)
        if not account:
            return None
        account.name = name
        if not await self.check_commit():
            return None
        await self._db.refresh(account)
        return account

    async def delete_account(self, account_id: int) -> bool:
        account = await self.get_account(account_id)
        if not account:
            return False
        await self._db.delete(account)
        await self._db.commit()
        return True
