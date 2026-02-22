from sqlalchemy import select
from sqlalchemy.orm import Session
from app.db.schema import User


class UserService:
    def __init__(self, session: Session):
        self._db = session

    def list_users(self) -> list[User]:
        result = self._db.execute(select(User))
        return result.scalars().all()

    def get_user(self, user_id: int) -> User | None:
        result = self._db.execute(select(User).where(User.id == user_id))
        return result.scalars().first()

    def check_name(self, name: str) -> bool:
        result = self._db.execute(select(User).where(User.name == name))
        return result.scalars().first() is not None

    def create_user(self, name: str) -> User:
        user = User(name=name)
        self._db.add(user)
        self._db.commit()
        self._db.refresh(user)
        return user

    def update_user(self, user_id: int, name: str) -> User | None:
        user = self.get_user(user_id)
        if not user:
            return None
        user.name = name
        self._db.commit()
        self._db.refresh(user)
        return user

    def delete_user(self, user_id: int) -> bool:
        user = self.get_user(user_id)
        if not user:
            return False
        self._db.delete(user)
        self._db.commit()
        return True
