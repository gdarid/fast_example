
def test_get_wrong_endpoint(client):
    response = client.get("/api/v100000/users/0")
    assert response.status_code == 404
