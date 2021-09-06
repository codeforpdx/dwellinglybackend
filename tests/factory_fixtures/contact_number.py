import pytest
from models.contact_number import ContactNumberModel
from tests.attributes import contact_number_attrs


@pytest.fixture
def contact_number_attributes(faker):
    def _contact_number_attributes():
        return contact_number_attrs(faker)

    yield _contact_number_attributes()


@pytest.fixture
def create_contact_number(contact_number_attributes, create_emergency_contact):
    def _create_contact_number(emergency_contact=None):
        if not emergency_contact:
            emergency_contact = create_emergency_contact()

        contact_number = ContactNumberModel(
            **contact_number_attributes, emergency_contact_id=emergency_contact.id
        )
        contact_number.save_to_db()
        return contact_number

    yield _create_contact_number
