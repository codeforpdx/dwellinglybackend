from tests.unit.base_interface_test import BaseInterfaceTest
from models.lease import LeaseModel
from schemas.lease import LeaseSchema


class TestBaseLeaseModel(BaseInterfaceTest):
    def setup(self):
        self.object = LeaseModel()
        self.custom_404_msg = "Lease not found"
        self.schema = LeaseSchema
