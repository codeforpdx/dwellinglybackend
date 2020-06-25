import pytest

def test_app(client, seeded_database):
    """A request sent to the root of the server should fail with 404 (not found)."""
    assert client.get("/").status_code == 404

def test_for_admins(client, empty_database):
    """A request sent when the database is empty should throw a server-side error ('Database unusable')."""
    with pytest.raises(Exception) as e_info:
        client.get("/api/tenants")
