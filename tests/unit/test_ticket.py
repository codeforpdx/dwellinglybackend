from tests.unit.base_interface_test import BaseInterfaceTest
from models.tickets import TicketModel
from schemas.ticket import TicketSchema

class TestBaseTicketModel(BaseInterfaceTest):
    def setup(self):
        self.object = TicketModel()
        self.custom_404_msg = 'Ticket not found'
        self.schema = TicketSchema
