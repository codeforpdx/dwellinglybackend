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

        invalid_tenant_validation_error = ["666 is not a valid tenant ID"]

        validation_errors = TicketSchema().validate(invalid_tenant)
        assert invalid_tenant_validation_error == validation_errors["tenant_id"]

    def test_validate_author(self):
        invalid_author = {"author_id": 888}

        invalid_author_validation_error = ["888 is not a valid user ID"]

        validation_errors = TicketSchema().validate(invalid_author)
        assert invalid_author_validation_error == validation_errors["author_id"]


class TestFixtures:
    def test_create_ticket(self, create_ticket):
        ticket = create_ticket()
        assert ticket
