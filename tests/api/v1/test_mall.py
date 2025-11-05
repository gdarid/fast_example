import pytest
from fastapi.testclient import TestClient

from app.api.v1.api_mall import get_mall_service
from app.main import app
from app.services.mall_service import MallService
from tests.set_test_db import TestingSessionLocal

# Setup the TestClient
client = TestClient(app)


# Dependency to override the get_db dependency in the main app
def override_get_mall_service():
    session = TestingSessionLocal()
    yield MallService(session=session)


app.dependency_overrides[get_mall_service] = override_get_mall_service

@pytest.fixture(scope="session")
def account_id() -> int:
    # Create a new account for malls
    response = client.post("/api/v1/accounts", json={"name": "Test Account for malls"})
    assert response.status_code == 200
    created_account = response.json()
    return created_account["id"]

def test_create_and_get_mall(account_id: int):
    # Create a new mall
    response = client.post("/api/v1/malls", json={"name": "Test Mall", "owner_id": account_id})
    assert response.status_code == 200
    created_mall = response.json()
    assert created_mall["name"] == "Test Mall"
    assert "id" in created_mall

    # Fetch the same mall
    get_response = client.get(f"/api/v1/malls/{created_mall['id']}")
    assert get_response.status_code == 200
    fetched_mall = get_response.json()
    assert fetched_mall["id"] == created_mall["id"]
    assert fetched_mall["name"] == "Test Mall"

    # Fetch malls
    get_response = client.get("/api/v1/malls")
    assert get_response.status_code == 200
    malls = get_response.json()
    assert len(malls) == 1
    assert malls[0]["id"] == created_mall["id"]
    assert malls[0]["name"] == "Test Mall"

def test_create_same_mall(account_id: int):
    # Create same mall
    response = client.post("/api/v1/malls", json={"name": "Test Mall", "owner_id": account_id})
    assert response.status_code == 409

def test_create_mall_with_wrong_account():
    # Create same mall
    response = client.post("/api/v1/malls", json={"name": "Test Mall wrong account", "owner_id": 0})
    assert response.status_code == 409

def test_create_update_delete_mall(account_id: int):
    response = client.post("/api/v1/malls", json={"name": "Test Mall 2", "owner_id": account_id})
    assert response.status_code == 200
    created_mall = response.json()

    response = client.put(f"/api/v1/malls/{created_mall['id']}",
                          json={"name": "Test Mall 2 - V1", "owner_id": account_id})
    assert response.status_code == 200

    response = client.put(f"/api/v1/malls/{created_mall['id']}", json={"name": "Test Mall 2 - V2", "owner_id": 0})
    assert response.status_code == 404  # wrong account

    response = client.delete(f"/api/v1/malls/{created_mall['id']}")
    assert response.status_code == 200

def test_get_wrong_mall():
    response = client.get("/api/v1/malls/0")
    assert response.status_code == 404

def test_update_wrong_mall():
    response = client.put("/api/v1/malls/0", json={"name": "Test Mall 2 - Updated"})
    assert response.status_code == 404

def test_delete_wrong_mall():
    response = client.delete("/api/v1/malls/0")
    assert response.status_code == 404

def test_get_mall_service():
    mall_service = get_mall_service()
    assert isinstance(mall_service, MallService)
