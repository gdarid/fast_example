import logging

from sqlalchemy.orm import Session
from sqlalchemy import exists
from sqlalchemy.exc import IntegrityError
from app.db.schema import Mall, Account


class MallService:
    def __init__(self, session: Session):
        self._db = session

    def check_commit(self) -> bool:
        try:
            self._db.commit()
        except IntegrityError:
            self._db.rollback()
            return False

        return True

    def list_malls(self) -> list[Mall]:
        return self._db.query(Mall).all()

    def get_mall(self, mall_id: int) -> Mall | None:
        return self._db.query(Mall).filter(Mall.id == mall_id).first()

    def check_name(self, name: str) -> bool:
        res = self._db.query(exists().where(Mall.name == name)).scalar()
        return res

    def create_mall(self, name: str, owner_id: int) -> Mall | None:
        account = self._db.query(Account).filter(Account.id == owner_id).first()
        if not account:
            logging.error("Account not found %s", owner_id)
            return None
        mall = Mall(name=name, owner_id=owner_id)
        self._db.add(mall)

        if not self.check_commit():
            return None

        self._db.refresh(mall)
        return mall

    def update_mall(self, mall_id: int, name: str, owner_id: int | None) -> Mall | None:
        mall = self.get_mall(mall_id)
        if not mall:
            return None
        if owner_id is not None:
            account = self._db.query(Account).filter(Account.id == owner_id).first()
            if not account:
                return None
            mall.owner_id = owner_id
        mall.name = name

        if not self.check_commit():
            return None

        self._db.refresh(mall)
        return mall

    def delete_mall(self, mall_id: int) -> bool:
        mall = self.get_mall(mall_id)
        if not mall:
            return False
        self._db.delete(mall)
        self._db.commit()
        return True
