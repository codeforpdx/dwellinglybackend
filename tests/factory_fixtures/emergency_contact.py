import pytest
from models.emergency_contact import EmergencyContactModel
from models.contact_number import ContactNumberModel


def emergency_contact_attrs(faker):
    return {
        "name": faker.name().upper(),
        "description": faker.sentence(nb_words=5),
    }


@pytest.fixture
def emergency_contact_attributes(faker, contact_number_attributes):
    def _emergency_contact_attributes():
        return {
            **emergency_contact_attrs(faker),
            "contact_numbers": [contact_number_attributes],
        }

    yield _emergency_contact_attributes()


@pytest.fixture
def create_emergency_contact(faker, contact_number_attributes):
    def _create_emergency_contact():
        emergency_contact = EmergencyContactModel(
            name=faker.name().upper(),
            description=faker.sentence(nb_words=5),
            contact_numbers=[ContactNumberModel(**contact_number_attributes)],
        )
        emergency_contact.save_to_db()
        return emergency_contact

    yield _create_emergency_contact
