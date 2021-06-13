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

    def test_property_manager_is_denied_access(self, pm_header, create_join_staff):
        payload = {
            "user_id": create_join_staff().id,
            "subject": "PM's email subject",
            "body": "I'm a property manager",
        }
        response = self.client.post(self.endpoint, json=payload, headers=pm_header)
        assert is_valid(response, 401)

    def test_admin_is_allowed_access(self, admin_header, create_join_staff):
        payload = {
            "user_id": create_join_staff().id,
            "subject": "Admin's email subject",
            "body": "I'm an admin",
        }
        response = self.client.post(self.endpoint, json=payload, headers=admin_header)
        assert is_valid(response, 200)

    def test_staff_is_denied_access(self, staff_header, create_join_staff):
        payload = {
            "user_id": create_join_staff().id,
            "subject": "Staff's email subject",
            "body": "I'm staff",
        }
        response = self.client.post(self.endpoint, json=payload, headers=staff_header)
        assert is_valid(response, 401)
