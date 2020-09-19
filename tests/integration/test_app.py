import pytest

def test_app(client, test_database):
    """A request sent to the root of the server should fail with 404 (not found)."""
    assert client.get("/").status_code == 404
