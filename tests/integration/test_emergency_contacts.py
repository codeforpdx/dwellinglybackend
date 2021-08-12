import pytest
from unittest.mock import patch
from conftest import is_valid
from models.emergency_contact import EmergencyContactModel
from schemas.emergency_contact import EmergencyContactSchema

endpoint = "/api/emergencycontacts"


@pytest.mark.usefixtures("client_class", "empty_test_db")
class TestEmergencyContactGet:
    def test_get(self, valid_header, create_emergency_contact):
        contact = create_emergency_contact()
        with patch.object(
            EmergencyContactModel, "find", return_value=contact
        ) as mock_find:
            response = self.client.get(f"{endpoint}/4321", headers=valid_header)

        mock_find.assert_called_once_with(4321)
        assert response.status_code == 200
        assert response.json == contact.json()


@pytest.mark.usefixtures("client_class", "empty_test_db")
class TestEmergencyContactsDelete:
    def test_get(self, valid_header, create_emergency_contact):
        with patch.object(EmergencyContactModel, "delete") as mock_delete:
            response = self.client.delete(f"{endpoint}/8745", headers=valid_header)

        mock_delete.assert_called_once_with(8745)
        assert response.status_code == 200
        assert response.json == {"message": "Emergency contact deleted"}


@pytest.mark.usefixtures("client_class", "empty_test_db")
class TestEmergencyContactsPost:
    def test_post(self, valid_header, create_emergency_contact):
        contact = create_emergency_contact()
        with patch.object(
            EmergencyContactModel, "create", return_value=contact
        ) as mock_create:
            response = self.client.post(
                endpoint, json={"yes": "ok"}, headers=valid_header
            )

        mock_create.assert_called_once_with(
            schema=EmergencyContactSchema, payload={"yes": "ok"}
        )
        assert response.status_code == 201
        assert response.json == contact.json()


@pytest.mark.usefixtures("client_class", "empty_test_db")
class TestEmergencyContactsGet:
    def test_get(self, valid_header, create_emergency_contact):
        contact = create_emergency_contact()
        response = self.client.get(endpoint, headers=valid_header)

        assert response.status_code == 200
        assert response.json == {"emergency_contacts": [contact.json()]}


@pytest.mark.skip(
    reason="This is testing a successful update action on a non-existent id..."
)
def test_emergency_contacts_PUT(client, valid_header, empty_test_db):
    id = 1
    updatedInfo = {
        "name": "Greg",
        "contact_numbers": [
            {"number": "503-291-9111", "numtype": "Call"},
            {"number": "503-555-3321", "numtype": "Text"},
        ],
    }

    response = client.put(f"{endpoint}/{id}", json=updatedInfo, headers=valid_header)
    assert is_valid(response, 200)  # OK
    assert response.json["name"] == "Greg"
    # assert response.json['contact_numbers'][0]['number'] == '503-291-9111'
    # This test will fail, Contact Numbers need an id in order to be updated.
    # The request is not submitting an id.
    # TODO: Create issue to address non restful behavior.

    id = 100
    response = client.put(f"{endpoint}/{id}", json=updatedInfo, headers=valid_header)
    assert is_valid(response, 404)  # NOT FOUND
    assert response.json == {"message": "Emergency contact not found"}
