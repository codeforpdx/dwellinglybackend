import pytest
from models.emergency_contact import EmergencyContactModel
from models.contact_number import ContactNumberModel


@pytest.fixture
def create_emergency_contact(faker, contact_number_attributes):
    def _create_emergency_contact():
        emergency_contact = EmergencyContactModel(
            name=(faker.name().upper()),
            description=faker.sentence(nb_words=5),
            contact_numbers=[ContactNumberModel(**contact_number_attributes)],
        )
        emergency_contact.save_to_db()
        return emergency_contact

    yield _create_emergency_contact
