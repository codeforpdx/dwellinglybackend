import pytest
from models.contact_number import ContactNumberModel
from schemas.contact_number import ContactNumberSchema
from tests.unit.base_interface_test import BaseInterfaceTest

emergency_contact_id = 1
number = "503-291-9111"
numtype = "Call"
extension = "356"


class TestBaseContactNumberModel(BaseInterfaceTest):
    def setup(self):
        self.object = ContactNumberModel()
        self.custom_404_msg = 'Lease not found'
        self.schema = ContactNumberSchema


class TestContactNumberModel():
    def test_contact_number(self):
        contact_number = ContactNumberModel(emergency_contact_id, number, numtype, extension)
        assert contact_number.emergency_contact_id == emergency_contact_id
        assert contact_number.number == number
        assert contact_number.numtype == numtype
        assert contact_number.extension == extension

@pytest.mark.usefixtures("empty_test_db")
class TestFixtures:
    def test_create_contact_number(self, create_contact_number):
        assert create_contact_number()

