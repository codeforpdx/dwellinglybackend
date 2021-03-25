from utils.time import Time
import pytest


@pytest.mark.usefixtures("client_class", "empty_test_db")
class TestLeaseAuthorizations:
    def valid_payload(self, tenant_id, property_id):
        return {
            "dateTimeStart": Time.today_iso(),
            "dateTimeEnd": Time.one_year_from_now_iso(),
            "tenantID": tenant_id,
            "propertyID": property_id,
        }

    # Test auth is in place at each endpoint
    def test_unauthorized_get_request(self):
        response = self.client.get("/api/lease/1")

        assert response.status_code == 401

    def test_unauthorized_get_all_request(self):
        response = self.client.get("/api/lease")

        assert response.status_code == 401

    def test_unauthorized_create_request(self):
        response = self.client.post("/api/lease")

        assert response.status_code == 401

    def test_unauthorized_delete_request(self):
        response = self.client.delete("/api/lease/1")

        assert response.status_code == 401

    def test_unauthorized_update_request(self):
        response = self.client.put("/api/lease/1")

        assert response.status_code == 401

    # Test all roles are authorized to access each endpoint
    def test_pm_authorized_to_get(self, pm_header, create_lease):
        lease = create_lease()

        response = self.client.get(f"/api/lease/{lease.id}", headers=pm_header)
        assert response.status_code == 200

    def test_staff_are_authorized_to_get(self, staff_header, create_lease):
        lease = create_lease()

        response = self.client.get(f"/api/lease/{lease.id}", headers=staff_header)
        assert response.status_code == 200

    def test_admin_is_authorized_to_get(self, admin_header, create_lease):
        lease = create_lease()

        response = self.client.get(f"/api/lease/{lease.id}", headers=admin_header)
        assert response.status_code == 200

    def test_pm_is_authorized_to_get_all(self, pm_header, create_lease):

        response = self.client.get("/api/lease", headers=pm_header)
        assert response.status_code == 200

    def test_staff_are_authorized_to_get_all(self, staff_header, create_lease):

        response = self.client.get("/api/lease", headers=staff_header)
        assert response.status_code == 200

    def test_admin_is_authorized_to_get_all(self, admin_header, create_lease):

        response = self.client.get("/api/lease", headers=admin_header)
        assert response.status_code == 200

    def test_pm_is_authorized_to_create(
        self, pm_header, create_tenant, create_property
    ):
        tenant = create_tenant()
        propertyID = create_property().id
        response = self.client.post(
            "/api/lease",
            json=self.valid_payload(tenant.id, propertyID),
            headers=pm_header,
        )

        assert response.status_code == 201

    def test_staff_are_authorized_to_create(
        self, staff_header, create_tenant, create_property
    ):
        tenant = create_tenant()
        propertyID = create_property().id
        response = self.client.post(
            "/api/lease",
            json=self.valid_payload(tenant.id, propertyID),
            headers=staff_header,
        )
        assert response.status_code == 201

    def test_admin_is_authorized_to_create(
        self, admin_header, create_tenant, create_property
    ):
        tenant = create_tenant()
        propertyID = create_property().id
        response = self.client.post(
            "/api/lease",
            json=self.valid_payload(tenant.id, propertyID),
            headers=admin_header,
        )
        assert response.status_code == 201

    def test_pm_is_authorized_to_delete_lease(self, pm_header, create_lease):
        lease = create_lease()
        response = self.client.delete(
            f"/api/lease/{lease.id}".format(id), headers=pm_header
        )

        assert response.status_code == 200

    def test_staff_are_authorized_to_delete_lease(self, staff_header, create_lease):
        lease = create_lease()
        response = self.client.delete(
            f"/api/lease/{lease.id}".format(id), headers=staff_header
        )

        assert response.status_code == 200

    def test_admin_is_authorized_to_delete_lease(self, admin_header, create_lease):
        lease = create_lease()
        response = self.client.delete(
            f"/api/lease/{lease.id}".format(id), headers=admin_header
        )

        assert response.status_code == 200

    def test_pm_is_authorized_to_update(self, pm_header, create_lease):
        lease = create_lease()
        payload = {
            "dateTimeStart": Time.today_iso(),
            "dateTimeEnd": Time.one_year_from_now_iso(),
        }
        response = self.client.put(
            f"/api/lease/{lease.id}", json=payload, headers=pm_header
        )
        assert response.status_code == 200

    def test_staff_authorized_to_update(self, staff_header, create_lease):
        lease = create_lease()
        payload = {
            "dateTimeStart": Time.today_iso(),
            "dateTimeEnd": Time.one_year_from_now_iso(),
        }
        response = self.client.put(
            f"/api/lease/{lease.id}", json=payload, headers=staff_header
        )
        assert response.status_code == 200

    def test_admin_authorized_to_update(self, admin_header, create_lease):
        lease = create_lease()
        payload = {
            "dateTimeStart": Time.today_iso(),
            "dateTimeEnd": Time.one_year_from_now_iso(),
        }
        response = self.client.put(
            f"/api/lease/{lease.id}", json=payload, headers=admin_header
        )
        assert response.status_code == 200
