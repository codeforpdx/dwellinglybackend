from conftest import is_valid
import pytest


@pytest.mark.usefixtures("client_class", "empty_test_db")
class TestEmergenyContactsAuthorizations:
    def setup(self):
        self.endpoint = "/api/emergencycontacts"

        self.newContact = {
            "name": "Narcotics Anonymous",
            "description": "Cool description",
            "contact_numbers": [
                {"number": "503-291-9111", "numtype": "Call"},
                {"number": "503-555-3321", "numtype": "Text"},
            ],
        }

        self.user_id = 1

    def test_auth_header_is_required(self):
        response = self.client.post(self.endpoint, json=self.newContact)

        assert is_valid(response, 401)
        assert response.json == {"message": "Missing authorization header"}

        response = self.client.delete(f"{self.endpoint}/{self.user_id}")
        assert is_valid(response, 401)
        assert response.json == {"message": "Missing authorization header"}

    def test_prop_manager_denied_emerg_contacts_POST(self, pm_header):
        response = self.client.post(
            self.endpoint, json=self.newContact, headers=pm_header
        )
        assert is_valid(response, 401)  # UNAUTHORIZED - Admin Access Required

    def test_prop_manager_denied_emerg_contacts_DELETE(self, pm_header):
        response = self.client.delete(
            f"{self.endpoint}/{self.user_id}", headers=pm_header
        )
        assert is_valid(response, 401)  # UNAUTHORIZED - Admin Access Required

    def test_staff_denied_emerg_contacts_POST(self, staff_header):
        response = self.client.post(
            self.endpoint, json=self.newContact, headers=staff_header
        )
        assert is_valid(response, 401)  # UNAUTHORIZED - Admin Access Required

    def test_staff_denied_emerg_contacts_DELETE(self, staff_header):
        response = self.client.delete(
            f"{self.endpoint}/{self.user_id}", headers=staff_header
        )
        assert is_valid(response, 401)  # UNAUTHORIZED - Admin Access Required

    def test_admin_allowed_emerg_contacts_POST(self, admin_header):
        response = self.client.post(
            self.endpoint, json=self.newContact, headers=admin_header
        )
        assert is_valid(response, 201)

    def test_admin_allowed_emerg_contacts_DELETE(
        self, admin_header, create_emergency_contact
    ):
        response = self.client.delete(
            f"{self.endpoint}/{create_emergency_contact().id}", headers=admin_header
        )
        assert is_valid(response, 200)
