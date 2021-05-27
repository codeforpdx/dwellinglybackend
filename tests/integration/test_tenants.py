import pytest
from models.tenant import TenantModel


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

    def test_create_tenant(self, valid_header):
        response = self.client.post(
            self.endpoint, json=self.new_tenant, headers=valid_header
        )

        assert response.json == TenantModel.find(response.json["id"]).json()
