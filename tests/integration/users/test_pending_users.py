import pytest


@pytest.mark.usefixtures("empty_test_db")
class TestPendingUsers:
    def test_users_pending(self, client, valid_header, create_unauthorized_user):
        pending_user = create_unauthorized_user()
        assert pending_user.role is None
        assert pending_user.archived is False

        """The get pending users returns one user with no role
        and a successful response code."""
        response = client.get(
            "/api/users/pending",
            headers=valid_header,
        )
        print(response)
        assert len(response.get_json()["users"]) == 1
        assert response.status_code == 200
