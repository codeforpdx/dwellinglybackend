from tests.unit.base_interface_test import BaseInterfaceTest
from models.tickets import TicketModel
from schemas.ticket import TicketSchema

class TestBaseTicketModel(BaseInterfaceTest):
    def setup(self):
        self.object = TicketModel()
        self.custom_404_msg = 'Ticket not found'
        self.schema = TicketSchema

    def test_validate_tenant(self):
        invalid_tenant = {
            'tenantID': 666
        }

        invalid_tenant_validation_error = {'tenantID': ['666 is not a valid tenant ID']}
        assert invalid_tenant_validation_error == TicketSchema().validate(invalid_tenant)

    def test_validate_assigned_user_and_sender(self):
        invalid_assigned_user_and_sender = {
            'assignedUserID': 777,
            'senderID': 888
        }

        invalid_assigned_user_validation_error = {'assignedUserID': ['777 is not a valid user ID'], 'senderID': ['888 is not a valid user ID']}
        assert invalid_assigned_user_validation_error == TicketSchema().validate(invalid_assigned_user_and_sender)

