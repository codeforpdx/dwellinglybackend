import pytest
from models.emergency_contact import EmergencyContactModel
from schemas.emergency_contact import EmergencyContactSchema
from tests.unit.base_interface_test import BaseInterfaceTest
from utils.time import Time


class TestBaseEmergencyContactModel(BaseInterfaceTest):
    def setup(self):
        self.object = EmergencyContactModel()
        self.custom_404_msg = 'EmergencyContact not found'
        self.schema = EmergencyContactSchema


@pytest.mark.usefixtures("empty_test_db")
class TestEmergencyContactModel:
    def test_emergency_contact_json(self, create_emergency_contact):
        emergency_contact = create_emergency_contact()
        assert emergency_contact.json() == {
            'name': emergency_contact.name,
            'contact_numbers': [number.json() for number in emergency_contact.contact_numbers],
            'description': emergency_contact.description,
            "created_at": Time.format_date(emergency_contact.created_at),
            "updated_at": Time.format_date(emergency_contact.updated_at)
        }


@pytest.mark.usefixtures("empty_test_db")
class TestFixtures:
    def test_create_emergency_contact(self, create_emergency_contact):
        assert create_emergency_contact()
