from conftest import is_valid
import pytest


@pytest.mark.usefixtures("client_class", "empty_test_db")
class TestEmergenyContactsAuthorizations:
    def setup(self):
        self.endpoint = "/api/emergencycontacts"

    def test_emergency_contacts_POST(self, auth_headers):
        endpoint = "/api/emergencycontacts"

        newContact = {
            "name": "Narcotics Anonymous",
            "description": "Cool description",
            "contact_numbers": [
                {"number": "503-291-9111", "numtype": "Call"},
                {"number": "503-555-3321", "numtype": "Text"},
            ],
        }

        response = self.client.post(
            endpoint, json=newContact, headers=auth_headers["pm"]
        )
        assert is_valid(response, 401)  # UNAUTHORIZED - Admin Access Required

        response = self.client.post(endpoint, json=newContact)
        assert is_valid(response, 401)  # UNAUTHORIZED - Missing Authorization Header
        assert response.json == {"message": "Missing authorization header"}

    def test_emergency_contacts_DELETE(self, auth_headers):
        endpoint = "/api/emergencycontacts"

        id = 1

        response = self.client.delete(f"{endpoint}/{id}")
        assert is_valid(response, 401)  # UNAUTHORIZED - Missing Authorization Header
        assert response.json == {"message": "Missing authorization header"}

        response = self.client.delete(f"{endpoint}/{id}", headers=auth_headers["pm"])
        assert is_valid(response, 401)  # UNAUTHORIZED - Admin Access Required
