from app.api.v1.api_account import get_account_service
from app.services.account_service import AccountService

# Predefined fixture : client

def test_create_and_get_account(client):
    # Create a new account
    response = client.post("/api/v1/accounts", json={"name": "Test Account"})
    assert response.status_code == 200
    created_account = response.json()
    assert created_account["name"] == "Test Account"
    assert "id" in created_account

    # Fetch the same account
    get_response = client.get(f"/api/v1/accounts/{created_account['id']}")
    assert get_response.status_code == 200
    fetched_account = get_response.json()
    assert fetched_account["id"] == created_account["id"]
    assert fetched_account["name"] == "Test Account"

    # Fetch accounts
    get_response = client.get("/api/v1/accounts")
    assert get_response.status_code == 200
    accounts = get_response.json()
    assert len(accounts) == 1
    assert accounts[0]["id"] == created_account["id"]
    assert accounts[0]["name"] == "Test Account"

def test_create_same_account(client):
    # Create same account
    response = client.post("/api/v1/accounts", json={"name": "Test Account"})
    assert response.status_code == 409

def test_create_update_delete_account(client):
    response = client.post("/api/v1/accounts", json={"name": "Test Account 2"})
    assert response.status_code == 200
    created_account = response.json()

    response = client.put(f"/api/v1/accounts/{created_account['id']}", json={"name": "Test Account 2 - Updated"})
    assert response.status_code == 200

    response = client.delete(f"/api/v1/accounts/{created_account['id']}")
    assert response.status_code == 200

def test_get_wrong_account(client):
    response = client.get("/api/v1/accounts/0")
    assert response.status_code == 404

def test_update_wrong_account(client):
    response = client.put("/api/v1/accounts/0", json={"name": "Test Account 2 - Updated"})
    assert response.status_code == 404

def test_delete_wrong_account(client):
    response = client.delete("/api/v1/accounts/0")
    assert response.status_code == 404

def test_get_account_service():
    account_service = get_account_service()
    assert isinstance(account_service, AccountService)
