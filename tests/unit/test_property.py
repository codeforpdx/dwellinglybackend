from tests.unit.base_interface_test import BaseInterfaceTest
from models.property import PropertyModel
from schemas.property import PropertySchema


class TestBasePropertyModel(BaseInterfaceTest):
    def setup(self):
        self.object = PropertyModel()
        self.custom_404_msg = "Property not found"
        self.schema = PropertySchema
