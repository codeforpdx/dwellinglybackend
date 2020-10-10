from db import db
from models.base_model import BaseModel
from tests.unit.base_interface_test import BaseInterfaceTest
from marshmallow import Schema


class TestBaseModel(BaseInterfaceTest):

    def setup(self):
        self.object = BaseModel()
        self.custom_404_msg = 'Base not found'
        self.schema = Schema()
