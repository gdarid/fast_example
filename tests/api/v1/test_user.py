from app.api.v1.api_user import get_user_service
from app.services.user_service import UserService

# Predefined fixture : client

def test_create_and_get_user(client):
    # Create a new user
    response = client.post("/api/v1/users", json={"name": "Test User"})
    assert response.status_code == 200
    created_user = response.json()
    assert created_user["name"] == "Test User"
    assert "id" in created_user

    # Fetch the same user
    get_response = client.get(f"/api/v1/users/{created_user['id']}")
    assert get_response.status_code == 200
    fetched_user = get_response.json()
    assert fetched_user["id"] == created_user["id"]
    assert fetched_user["name"] == "Test User"

    # Fetch users
    get_response = client.get("/api/v1/users")
    assert get_response.status_code == 200
    users = get_response.json()
    assert len(users) == 1
    assert users[0]["id"] == created_user["id"]
    assert users[0]["name"] == "Test User"

def test_create_same_user(client):
    # Create same user
    response = client.post("/api/v1/users", json={"name": "Test User"})
    assert response.status_code == 409

def test_create_update_delete_user(client):
    response = client.post("/api/v1/users", json={"name": "Test User 2"})
    assert response.status_code == 200
    created_user = response.json()

    response = client.put(f"/api/v1/users/{created_user['id']}", json={"name": "Test User 2 - Updated"})
    assert response.status_code == 200

    response = client.delete(f"/api/v1/users/{created_user['id']}")
    assert response.status_code == 200

def test_get_wrong_user(client):
    response = client.get("/api/v1/users/0")
    assert response.status_code == 404

def test_update_wrong_user(client):
    response = client.put("/api/v1/users/0", json={"name": "Test User 2 - Updated"})
    assert response.status_code == 404

def test_delete_wrong_user(client):
    response = client.delete("/api/v1/users/0")
    assert response.status_code == 404

def test_get_user_service():
    user_service = get_user_service()
    assert isinstance(user_service, UserService)
