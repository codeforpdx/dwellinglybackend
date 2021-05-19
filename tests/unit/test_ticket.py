from tests.unit.base_interface_test import BaseInterfaceTest
from models.tickets import TicketModel
from schemas.ticket import TicketSchema


class TestBaseTicketModel(BaseInterfaceTest):
    def setup(self):
        self.object = TicketModel()
        self.custom_404_msg = "Ticket not found"
        self.schema = TicketSchema

    def test_validate_tenant(self):
        invalid_tenant = {"tenant_id": 666}

        invalid_tenant_validation_error = {
            "tenant_id": ["666 is not a valid tenant ID"]
        }
        assert invalid_tenant_validation_error == TicketSchema().validate(
            invalid_tenant
        )

    def test_validate_creator(self):
        invalid_creator = {"creator_id": 888}

        invalid_creator_validation_error = {
            "creator_id": ["888 is not a valid user ID"],
        }
        assert invalid_creator_validation_error == TicketSchema().validate(
            invalid_creator
        )
