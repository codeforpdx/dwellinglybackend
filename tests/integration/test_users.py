def test_user_register(client):
    data = {
        "email": "user1@dwellingly.org",
        "password": "1234"
    }

    response = client.post("/api/login", json=data)

    assert response.status_code == 200
    assert response.content_type == "application/json"
    assert "access_token" in response.json.keys()
