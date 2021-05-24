import pytest
from models.tickets import TicketModel
from models.tickets import TicketStatus


@pytest.fixture
def ticket_attributes(faker):
    def _ticket_attributes(issue, tenant, creator):
        return {
            "issue": issue,
            "tenant_id": tenant.id,
            "author_id": creator.id,
            "status": TicketStatus.New,
            "urgency": faker.random_element(("Low", "Medium", "High")),
        }

    yield _ticket_attributes


@pytest.fixture
def create_ticket(faker, ticket_attributes, create_tenant, create_join_staff):
    def _create_ticket(issue=None):
        if not issue:
            issue = faker.sentence()
        tenant = create_tenant()
        ticket = TicketModel(**ticket_attributes(issue, tenant, create_join_staff()))
        ticket.save_to_db()
        return ticket

    yield _create_ticket
