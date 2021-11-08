import pytest
from conftest import is_valid


@pytest.mark.usefixtures("client_class")
class TestTenantAuthorization:
    def setup(self):
        self.endpoint = "/api/tenants"

    def test_post(self, create_join_staff, pm_header):
        staff_1 = create_join_staff()
        staff_2 = create_join_staff()
        newTenant = {
            "firstName": "Jake",
            "lastName": "The Dog",
            "phone": "111-111-1111",
            "staffIDs": [staff_1.id, staff_2.id],
        }
        response = self.client.post(self.endpoint, json=newTenant, headers=pm_header())
        assert is_valid(response, 401)  # UNAUTHORIZED - Admin Access Required

        response = self.client.post(self.endpoint, json=newTenant)
        # UNAUTHORIZED - Missing Authorization Header
        assert is_valid(response, 401)
        assert response.json == {"message": "Missing authorization header"}
