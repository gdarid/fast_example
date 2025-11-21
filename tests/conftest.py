import pytest
from fastapi.testclient import TestClient

from tests.set_test_db import TestingSessionLocal
from app.main import app
from app.services.account_service import AccountService
from app.services.user_service import UserService
from app.services.mall_service import MallService
from app.api.v1.api_account import get_account_service
from app.api.v1.api_user import get_user_service
from app.api.v1.api_mall import get_mall_service

# Centralized dependency overrides that close sessions
def override_get_account_service():
    session = TestingSessionLocal()
    try:
        yield AccountService(session=session)
    finally:
        session.close()

def override_get_user_service():
    session = TestingSessionLocal()
    try:
        yield UserService(session=session)
    finally:
        session.close()

def override_get_mall_service():
    session = TestingSessionLocal()
    try:
        yield MallService(session=session)
    finally:
        session.close()

@pytest.fixture(scope="session")
def client():
    # Install overrides just once for the test session
    app.dependency_overrides[get_account_service] = override_get_account_service
    app.dependency_overrides[get_user_service] = override_get_user_service
    app.dependency_overrides[get_mall_service] = override_get_mall_service

    with TestClient(app) as c:
        yield c
