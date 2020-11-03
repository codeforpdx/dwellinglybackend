import pytest
from models.tickets import TicketModel
from models.tickets import TicketStatus

@pytest.fixture
def ticket_attributes():
    def _ticket_attributes(issue, tenant, assignedUser, sender):
        return {
            "issue": issue,
            "tenant": tenant.id,
            "assignedUser": assignedUser.id,
            "sender": sender.id,
            "status": TicketStatus.New,
            "urgency": "high"
        }
    yield _ticket_attributes

@pytest.fixture
def create_ticket(ticket_attributes, create_tenant, assigned_user, sender):
    def _create_ticket(issue="Leaky pipe"):
        tenant = create_tenant()
        ticket = TicketModel(**ticket_attributes(issue, tenant, assigned_user, sender))
        ticket.save_to_db()
        return ticket
    yield _create_ticket