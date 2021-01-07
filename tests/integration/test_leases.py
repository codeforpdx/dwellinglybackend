import pytest
from models.lease import LeaseModel
from schemas.lease import LeaseSchema
from serializers.lease import LeaseSerializer
from utils.time import Time
from unittest.mock import patch


@pytest.mark.usefixtures("client_class", "empty_test_db")
class TestLease:
    def setup(self):
        self.endpoint = "/api/lease"

    def test_get_a_lease(self, valid_header, create_lease):
        lease = create_lease()
        with patch.object(LeaseModel, "find", return_value=lease) as mock_find:
            response = self.client.get(f"{self.endpoint}/1", headers=valid_header)

        mock_find.assert_called_once_with(1)
        assert response.status_code == 200
        assert response.json == LeaseSerializer.serialize(lease)

    def test_get_all_leases(self, valid_header, create_lease):
        lease = create_lease()
        second_lease = create_lease()

        response = self.client.get(self.endpoint, headers=valid_header)

        assert response.status_code == 200
        assert response.json == {
            "leases": [
                LeaseSerializer.serialize(lease),
                LeaseSerializer.serialize(second_lease),
            ]
        }

    def test_get_all_leases_when_no_leases(self, valid_header):
        response = self.client.get(self.endpoint, headers=valid_header)

        assert response.status_code == 200
        assert response.json == {"leases": []}

    def test_create_lease(self, valid_header):
        with patch.object(LeaseModel, "create") as mock_create:
            response = self.client.post(
                self.endpoint, json={"yes": "ok"}, headers=valid_header
            )

        mock_create.assert_called_once_with(schema=LeaseSchema, payload={"yes": "ok"})
        assert response.status_code == 201
        assert response.json == {"message": "Lease created successfully"}

    def test_delete_lease(self, valid_header):
        with patch.object(LeaseModel, "delete") as mock_delete:
            response = self.client.delete(f"{self.endpoint}/1", headers=valid_header)

        mock_delete.assert_called_once_with(1)
        assert response.status_code == 200
        assert response.json == {"message": "Lease deleted"}

    def test_update_lease(self, valid_header, create_lease):
        lease = create_lease()
        with patch.object(LeaseModel, "update", return_value=lease) as mock_update:
            response = self.client.put(
                f"{self.endpoint}/1", json={"hello": "world"}, headers=valid_header
            )

        mock_update.assert_called_once_with(
            schema=LeaseSchema, id=1, payload={"hello": "world"}
        )
        assert response.status_code == 200
        assert response.json == LeaseSerializer.serialize(lease)


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
