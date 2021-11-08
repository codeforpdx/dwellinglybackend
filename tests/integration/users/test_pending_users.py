class TestPendingUsers:
    def test_users_pending(self, client, valid_header, create_unauthorized_user):
        pending_user = create_unauthorized_user()

        """The get pending users returns one user with no role
        and a successful response code."""
        response = client.get(
            "/api/users/pending",
            headers=valid_header,
        )

        assert response.json == {"users": [pending_user.json()]}
        assert response.status_code == 200
