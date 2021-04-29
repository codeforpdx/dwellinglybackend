from conftest import is_valid
import pytest


@pytest.mark.usefixtures("client_class", "empty_test_db")
class TestEmailAuthorizations:
    def setup(self):
        self.endpoint = "/api/user/message"

    def test_auth_header_is_required(self):
        response = self.client.post(self.endpoint)

        assert is_valid(response, 401)
        assert response.json == {"message": "Missing authorization header"}

    def test_all_roles_except_admin_are_denied_access(self, auth_headers):
        payload = {"user_id": 1, "subject": "Some email subject", "body": "Some body"}
        for role, token in auth_headers.items():
            if role != "admin":
                response = self.client.post(self.endpoint, json=payload, headers=token)
                assert is_valid(response, 401)
