import pytest

def test_app(client, seeded_database):
    assert client.get("/").status_code == 404

def test_for_admins(client, empty_database):
    with pytest.raises(Exception) as e_info:
        client.get("/api/tenants")
