from typing import Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.db.schema import Account


class AccountService:
    def __init__(self, session: Session):
        self._db = session

    def check_commit(self) -> bool:
        try:
            self._db.commit()
        except IntegrityError:
            self._db.rollback()
            return False

        return True

    def list_accounts(self) -> Sequence[Account]:
        result = self._db.execute(select(Account))
        return result.scalars().all()

    def get_account(self, account_id: int) -> Account | None:
        result = self._db.execute(select(Account).where(Account.id == account_id))
        return result.scalars().first()

    def check_name(self, name: str) -> bool:
        result = self._db.execute(select(Account).where(Account.name == name))
        return result.scalars().first() is not None

    def create_account(self, name: str) -> Account | None:
        account = Account(name=name)
        self._db.add(account)
        if not self.check_commit():
            return None
        self._db.refresh(account)
        return account

    def update_account(self, account_id: int, name: str) -> Account | None:
        account = self.get_account(account_id)
        if not account:
            return None
        account.name = name
        if not self.check_commit():
            return None
        self._db.refresh(account)
        return account

    def delete_account(self, account_id: int) -> bool:
        account = self.get_account(account_id)
        if not account:
            return False
        self._db.delete(account)
        self._db.commit()
        return True
