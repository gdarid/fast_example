from sqlalchemy import exists
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

    def list_accounts(self) -> list[Account]:
        return self._db.query(Account).all()

    def get_account(self, account_id: int) -> Account | None:
        account = self._db.query(Account).filter(Account.id == account_id).first()
        return account

    def check_name(self, name: str) -> bool:
        res = self._db.query(exists().where(Account.name == name)).scalar()
        return res

    def create_account(self, name: str) -> Account:
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
