
def test_get_wrong_endpoint(client):
    response = client.get("/abcdefghijklm")
    assert response.status_code == 404
