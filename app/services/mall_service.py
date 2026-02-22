from sqlalchemy.orm import Session
from sqlalchemy import select
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
        result = self._db.execute(select(Mall))
        return result.scalars().all()

    def get_mall(self, mall_id: int) -> Mall | None:
        result = self._db.execute(select(Mall).where(Mall.id == mall_id))
        return result.scalars().first()

    def check_name(self, name: str) -> bool:
        result = self._db.execute(select(Mall).where(Mall.name == name))
        return result.scalars().first() is not None

    def create_mall(self, name: str, owner_id: int) -> Mall | None:
        result = self._db.execute(select(Account).where(Account.id == owner_id))
        account = result.scalars().first()
        if not account:
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
            result = self._db.execute(select(Account).where(Account.id == owner_id))
            account = result.scalars().first()
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
