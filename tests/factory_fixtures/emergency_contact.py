import pytest
from models.emergency_contact import EmergencyContactModel

@pytest.fixture
def create_emergency_contact(contact_number_attributes):
    def _create_emergency_contact():
        emergency_contact = EmergencyContactModel(
            name="EMS",
            description="For emergency health crises",
            contact_numbers=[contact_number_attributes]
        )
        emergency_contact.save_to_db()
        return emergency_contact
    yield _create_emergency_contact
