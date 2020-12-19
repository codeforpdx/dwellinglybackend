import pytest
from faker import Faker
from models.tickets import TicketModel
from models.tickets import TicketStatus

@pytest.fixture
def ticket_attributes():
    def _ticket_attributes(issue, tenant, assignedUser, sender):
        return {
            "issue": issue,
            "tenantID": tenant.id,
            "assignedUserID": assignedUser.id,
            "senderID": sender.id,
            "status": TicketStatus.New,
            "urgency": "high"
        }
    yield _ticket_attributes

@pytest.fixture
def create_ticket(ticket_attributes, create_tenant, create_admin_user, create_join_staff):
    fake = Faker()
    def _create_ticket(issue=fake.sentence()):
        tenant = create_tenant()
        ticket = TicketModel(**ticket_attributes(issue, tenant, create_admin_user(), create_join_staff()))
        ticket.save_to_db()
        return ticket
    yield _create_ticket

