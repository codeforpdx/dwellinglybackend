from db import db
from models.base_model import BaseModel
from tests.unit.base_interface_test import BaseInterfaceTest


class TestBaseModel(BaseInterfaceTest):

    def setup(self):
        self.object = BaseModel()
