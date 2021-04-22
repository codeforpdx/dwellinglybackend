import pytest
from conftest import is_valid


@pytest.mark.usefixtures("client_class", "empty_test_db")
class TestTenantAuthorization:
    def setup(self):
        self.endpoint = "/api/tenants"

    def test_post(self, create_join_staff, auth_headers):
        staff_1 = create_join_staff()
        staff_2 = create_join_staff()
        newTenant = {
            "firstName": "Jake",
            "lastName": "The Dog",
            "phone": "111-111-1111",
            "staffIDs": [staff_1.id, staff_2.id],
        }
        response = self.client.post(
            self.endpoint, json=newTenant, headers=auth_headers["pm"]
        )
        assert is_valid(response, 401)  # UNAUTHORIZED - Admin Access Required

        response = self.client.post(self.endpoint, json=newTenant)
        # UNAUTHORIZED - Missing Authorization Header
        assert is_valid(response, 401)
        assert response.json == {"message": "Missing authorization header"}

    def test_unauthenticated_delete(self):
        response = self.client.delete(f"{self.endpoint}/1")

        assert is_valid(response, 401)
        assert response.json == {"message": "Missing authorization header"}

    def test_pm_role_is_unauthorized_to_delete(self, auth_headers):
        response = self.client.delete(f"{self.endpoint}/1", headers=auth_headers["pm"])

        assert is_valid(response, 401)