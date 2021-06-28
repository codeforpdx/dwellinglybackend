import pytest
from unittest.mock import patch
from models.tenant import TenantModel
from schemas import TenantSchema


@pytest.mark.usefixtures("client_class", "empty_test_db")
class TestTenantGet:
    def setup(self):
        self.endpoint = "/api/tenants"

    def test_get(self, valid_header, create_tenant):
        tenant = create_tenant()

        response = self.client.get(f"{self.endpoint}/{tenant.id}", headers=valid_header)

        assert response.json == tenant.json()


@pytest.mark.usefixtures("client_class", "empty_test_db")
class TestTenantPut:
    def setup(self):
        self.endpoint = "/api/tenants"

    def test_update_tenant(self, valid_header, create_tenant):
        tenant = create_tenant()
        updated_fields = {"archived": True}

        with patch.object(TenantModel, "update", return_value=tenant) as mock_update:
            response = self.client.put(
                f"{self.endpoint}/{tenant.id}",
                json=updated_fields,
                headers=valid_header,
            )

        mock_update.assert_called_once_with(
            schema=TenantSchema, id=tenant.id, payload=updated_fields
        )
        assert response.status_code == 200
        assert response.json == tenant.json()


@pytest.mark.usefixtures("client_class", "empty_test_db")
class TestTenantsGet:
    def test_get_all_tenants(self, valid_header, create_tenant):
        tenant = create_tenant()
        tenant_two = create_tenant()

        response = self.client.get("/api/tenants", headers=valid_header)

        assert response.status_code == 200
        assert response.json == {"tenants": [tenant.json(), tenant_two.json()]}


@pytest.mark.usefixtures("client_class", "empty_test_db")
class TestTenantsPost:
    def test_create(
        self, valid_header, tenant_attributes, lease_payload, create_tenant
    ):
        tenant_attrs = tenant_attributes()
        lease_attrs = lease_payload()
        tenant = create_tenant()

        with patch.object(TenantModel, "create", return_value=tenant) as mock_create:
            response = self.client.post(
                "/api/tenants",
                json={**tenant_attrs, **lease_attrs},
                headers=valid_header,
            )

        mock_create.assert_called_once_with(
            schema=TenantSchema, payload={**tenant_attrs, "leases": [{**lease_attrs}]}
        )

        assert response.json == tenant.json()
        assert response.status_code == 201
