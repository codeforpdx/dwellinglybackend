import pytest
from models.contact_number import ContactNumberModel
from schemas.contact_number import ContactNumberSchema
from tests.unit.base_interface_test import BaseInterfaceTest
from utils.time import Time


class TestBaseContactNumberModel(BaseInterfaceTest):
    def setup(self):
        self.object = ContactNumberModel()
        self.custom_404_msg = 'ContactNumber not found'
        self.schema = ContactNumberSchema

@pytest.mark.usefixtures("empty_test_db")
class TestContactNumberModel:
    def test_contact_number_json_method(self, create_contact_number):
        contact_number = create_contact_number()
        assert contact_number.json() == {
            'id': contact_number.id,
            'number':contact_number.number,
            'numtype': contact_number.numtype,
            'extension': contact_number.extension,
            "created_at": Time.format_date(contact_number.created_at),
            "updated_at": Time.format_date(contact_number.updated_at)
        }


@pytest.mark.usefixtures("empty_test_db")
class TestFixtures:
    def test_create_contact_number(self, create_contact_number):
        assert create_contact_number()
