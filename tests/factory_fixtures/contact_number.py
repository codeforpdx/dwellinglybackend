import pytest
from models.contact_number import ContactNumberModel

@pytest.fixture
def contact_number_attributes():
    def _contact_number_attributes():
        return {
            "number": "555-555-5555",
            "numtype": "mobile",
            "extension": "1"
        }
    yield _contact_number_attributes()

@pytest.fixture
def create_contact_number(contact_number_attributes, create_emergency_contact):
    def _create_contact_number(emergency_contact=create_emergency_contact()):
        contact_number = ContactNumberModel(
            number="503-555-5555",
            numtype="mobile",
            extension="1",
            emergency_contact_id=emergency_contact.id
        )
        contact_number.save_to_db()
        return contact_number

    yield _create_contact_number


