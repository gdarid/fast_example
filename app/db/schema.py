""" Database schema """
from typing import Generator, Any
from sqlalchemy import ForeignKey, UniqueConstraint, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker, relationship

from app.core.config import config

sql_echo = True if config.sql_echo == "True" else config.sql_echo
sql_echo = False if config.sql_echo == "" else sql_echo

# Only set SQLite-specific connect_args for SQLite URLs
connect_args = {"check_same_thread": False} if config.db_url.startswith("sqlite") else {}

engine = create_engine(config.db_url, connect_args=connect_args, echo=sql_echo)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(index=True, unique=True)

    __table_args__ = (UniqueConstraint('name', name='_user_name_unique'), )

class Account(Base):
    __tablename__ = "account"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(index=True)

    malls: Mapped[list["Mall"]] = relationship(back_populates="owner")

    __table_args__ = (UniqueConstraint('name', name='_account_name_unique'),)


class Mall(Base):
    __tablename__ = "mall"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(index=True)

    owner_id: Mapped[int] = mapped_column(ForeignKey("account.id"))
    owner: Mapped["Account"] = relationship(back_populates="malls")

    __table_args__ = (UniqueConstraint('name', name='_mall_name_unique'), )


# Dependency helper for FastAPI to yield a DB session and close it after request
def get_session() -> Generator[Any, None, None]:
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
