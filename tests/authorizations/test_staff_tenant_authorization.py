import pytest


@pytest.mark.usefixtures("client_class", "empty_test_db")
class TestStaffTenantAuthorizations:
    def setup(self):
        self.endpoint = "/api/staff-tenants"

    @staticmethod
    def valid_payload(tenants, staff):
        return {"staff": staff, "tenants": tenants}

    def test_unauthorized_update_request(self, create_tenant, create_join_staff):
        response = self.client.patch(
            self.endpoint,
            json=TestStaffTenantAuthorizations.valid_payload(
                tenants=[create_tenant().id], staff=[create_join_staff().id]
            ),
        )

        assert response.status_code == 401

    def test_pm_is_unauthorized(self, pm_header, create_tenant, create_join_staff):
        response = self.client.patch(
            self.endpoint,
            json=TestStaffTenantAuthorizations.valid_payload(
                tenants=[create_tenant().id], staff=[create_join_staff().id]
            ),
            headers=pm_header,
        )

        assert response.status_code == 401

    def test_staff_is_unauthorized(
        self, staff_header, create_tenant, create_join_staff
    ):
        response = self.client.patch(
            self.endpoint,
            json=TestStaffTenantAuthorizations.valid_payload(
                tenants=[create_tenant().id], staff=[create_join_staff().id]
            ),
            headers=staff_header,
        )

        assert response.status_code == 401

    def test_admin_is_authorized(self, admin_header, create_tenant, create_join_staff):
        response = self.client.patch(
            self.endpoint,
            json=TestStaffTenantAuthorizations.valid_payload(
                tenants=[create_tenant().id], staff=[create_join_staff().id]
            ),
            headers=admin_header,
        )

        assert response.status_code == 200
