import pytest
from models.contact_number import ContactNumberModel


@pytest.fixture
def contact_number_attributes(faker):
    def _contact_number_attributes():
        return {
            "number": faker.phone_number(),
            "numtype": faker.random_element(("home", "work", "mobile")),
            "extension": faker.bothify(text="?###"),
        }

    yield _contact_number_attributes()


@pytest.fixture
def create_contact_number(contact_number_attributes, create_emergency_contact):
    emergency_contact = create_emergency_contact()

    def _create_contact_number(emergency_contact=emergency_contact):
        contact_number = ContactNumberModel(
            **contact_number_attributes, emergency_contact_id=emergency_contact.id
        )
        contact_number.save_to_db()
        return contact_number

    yield _create_contact_number
