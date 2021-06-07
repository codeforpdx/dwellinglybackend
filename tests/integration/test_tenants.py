import pytest
from conftest import is_valid
from models.tenant import TenantModel
from schemas.tenant import TenantSchema
from utils.time import Time
from unittest.mock import patch

endpoint = "/api/tenants"


def test_tenants_GET_all(client, test_database, auth_headers):
    response = client.get(endpoint, headers=auth_headers["admin"])
    assert is_valid(response, 200)  # OK
    assert response.json["tenants"][0]["firstName"] == "Renty"


def test_tenants_GET_one(client, test_database, auth_headers):
    id = 1
    response = client.get(f"{endpoint}/{id}", headers=auth_headers["admin"])
    assert is_valid(response, 200)  # OK
    assert response.json["firstName"] == "Renty"

    id = 100
    response = client.get(f"{endpoint}/{id}", headers=auth_headers["admin"])
    assert is_valid(response, 404)  # NOT FOUND - 'Tenant not found'
    assert response.json == {"message": "Tenant not found"}


def test_tenants_POST(
    client,
    empty_test_db,
    auth_headers,
    valid_header,
    create_property,
    create_join_staff,
):
    staff_1 = create_join_staff()
    staff_2 = create_join_staff()
    newTenant = {
        "firstName": "Jake",
        "lastName": "The Dog",
        "phone": "111-111-1111",
        "staffIDs": [staff_1.id, staff_2.id],
    }

    newTenantWithLease = {
        "firstName": "Finn",
        "lastName": "The Human",
        "phone": "123-555-4321",
        "propertyID": create_property().id,
        "occupants": 3,
        "dateTimeEnd": Time.one_year_from_now_iso(),
        "dateTimeStart": Time.yesterday_iso(),
        "unitNum": "413",
    }

    response = client.post(endpoint, json=newTenant, headers=valid_header)

    assert is_valid(response, 201)  # CREATED
    assert response.json["firstName"] == "Jake"

    response = client.post(endpoint, json=newTenantWithLease, headers=valid_header)
    assert is_valid(response, 201)
    assert response.json["unitNum"] == "413"

    response = client.post(endpoint, json=newTenant, headers=valid_header)


@pytest.mark.usefixtures("client_class", "empty_test_db")
class TestTenant:
    def setup(self):
        self.endpoint = "/api/tenants"

    def test_update_tenant(self, empty_test_db, valid_header, create_tenant):
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
