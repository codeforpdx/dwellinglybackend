import pytest
from models.tenant import TenantModel
from unittest.mock import patch

from schemas import TenantSchema


@pytest.mark.usefixtures("client_class", "empty_test_db")
class TestGet:
    def setup(self):
        self.endpoint = "/api/tenants"

    def test_get_tenant(self, valid_header, create_tenant):
        tenant = create_tenant()

        response = self.client.get(f"{self.endpoint}/{tenant.id}", headers=valid_header)

        assert response.json == tenant.json()


@pytest.mark.usefixtures("client_class", "empty_test_db")
class TestPut:
    def setup(self):
        self.endpoint = "/api/tenants"

    def test_update_tenant(self, valid_header, create_tenant):
        tenant = create_tenant()
        updated_fields = {"archived": True}

        response = self.client.put(
            f"{self.endpoint}/{tenant.id}",
            json=updated_fields,
            headers=valid_header,
        )

        assert response.json == tenant.json()


@pytest.mark.usefixtures("client_class", "empty_test_db")
class TestGetAll:
    def setup(self):
        self.endpoint = "/api/tenants"

    def test_get_all_tenants(self, valid_header, create_tenant):
        create_tenant()
        create_tenant()
        all_tenants = TenantModel.query.json()

        response = self.client.get(self.endpoint, headers=valid_header)

        assert response.json["tenants"] == all_tenants


@pytest.mark.usefixtures("client_class", "empty_test_db")
class TestCreate:
    def setup(self):
        self.endpoint = "/api/tenants"
        self.new_tenant = {
            "firstName": "Testy",
            "lastName": "McTesterson",
            "phone": "1234567890",
            "archived": False,
        }

    def test_create_tenant(self, valid_header, create_tenant):

        with patch.object(
            TenantModel, "create", return_value=create_tenant()
        ) as mock_create:
            response = self.client.post(
                self.endpoint, json=self.new_tenant, headers=valid_header
            )

        mock_create.assert_called_once_with(
            schema=TenantSchema, payload=self.new_tenant
        )

        assert response.status_code == 201

    def test_create_tenant_with_lease(
        self, valid_header, create_property, create_lease
    ):
        lease = {
            "occupants": 47,
            "dateTimeStart": "2021-06-19T07:00:00.000Z",
            "dateTimeEnd": "2022-07-16T07:00:00.000Z",
            "unitNum": "5351",
            "propertyID": create_property().id,
        }

        response = self.client.post(
            self.endpoint, json={**self.new_tenant, **lease}, headers=valid_header
        )

        assert response.status_code == 201
        assert response.json["firstName"] == self.new_tenant["firstName"]
        assert response.json["lastName"] == self.new_tenant["lastName"]
        assert response.json["phone"] == self.new_tenant["phone"]
        assert response.json["unitNum"] == lease["unitNum"]
        assert response.json["occupants"] == lease["occupants"]
