# import pytest
import pytest_asyncio
from fastapi.testclient import TestClient

from tests.set_test_db import TestingSessionLocal
from main import app
from app.services.account_service import AccountService
from app.services.user_service import UserService
from app.services.mall_service import MallService
from app.api.v1.api_account import get_account_service
from app.api.v1.api_user import get_user_service
from app.api.v1.api_mall import get_mall_service

# Centralized dependency overrides that close sessions
async def override_get_account_service():
    async with TestingSessionLocal() as session:
        yield AccountService(session=session)

async def override_get_user_service():
    async with TestingSessionLocal() as session:
        yield UserService(session=session)

async def override_get_mall_service():
    async with TestingSessionLocal() as session:
        yield MallService(session=session)

@pytest_asyncio.fixture(scope="session")
def client():
    # Install overrides just once for the test session
    app.dependency_overrides[get_account_service] = override_get_account_service
    app.dependency_overrides[get_user_service] = override_get_user_service
    app.dependency_overrides[get_mall_service] = override_get_mall_service

    with TestClient(app) as c:
        yield c

@pytest_asyncio.fixture(scope="session")
def session_local():
    return TestingSessionLocal()
