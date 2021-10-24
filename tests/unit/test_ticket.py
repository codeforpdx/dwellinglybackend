import pytest

from tests.unit.base_interface_test import BaseInterfaceTest
from models.tickets import TicketModel
from schemas.ticket import TicketSchema
from utils.time import TimeStamp


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


@pytest.mark.usefixtures("empty_test_db")
class TestFixtures:
    def test_create_ticket(self, create_ticket):
        ticket = create_ticket()
        assert ticket

        ticket = create_ticket(status=TicketModel.NEW)
        assert ticket.status == "New"

        ticket = create_ticket(status=TicketModel.IN_PROGRESS)
        assert ticket.status == "In Progress"

        ticket = create_ticket(status=TicketModel.CLOSED)
        assert ticket.status == "Closed"

        one_week_ago = TimeStamp.weeks_ago(1)
        ticket = create_ticket(created_at=one_week_ago)
        assert ticket.created_at.__str__() == one_week_ago
