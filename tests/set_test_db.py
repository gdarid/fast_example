import asyncio

from sqlalchemy import StaticPool  # , create_engine
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

# from sqlalchemy.orm import sessionmaker

from app.db.schema import Base

# Setup the in-memory SQLite database for testing
DATABASE_URL = "sqlite+aiosqlite:///:memory:"
# engine = create_engine(
#     DATABASE_URL,
#     connect_args={
#         "check_same_thread": False,
#     },
#     poolclass=StaticPool,
# )
# TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

engine = create_async_engine(DATABASE_URL, connect_args={"check_same_thread": False}, poolclass=StaticPool)
TestingSessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False, )

# Base.metadata.create_all(bind=engine)

async def init_models(eng):
    async with eng.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

asyncio.run(init_models(engine))
