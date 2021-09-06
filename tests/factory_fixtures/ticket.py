import pytest
from models.tickets import TicketModel
from schemas.ticket import TicketSchema
from tests.attributes import ticket_attrs


@pytest.fixture
def ticket_attributes(faker, create_tenant, create_join_staff):
    def _ticket_attributes(issue=None, tenant=None, author=None):
        return {
            **ticket_attrs(faker),
            "tenant_id": tenant.id if tenant else create_tenant().id,
            "author_id": author.id if author else create_join_staff().id,
        }

    yield _ticket_attributes


@pytest.fixture
def create_ticket(faker, ticket_attributes, create_tenant, create_join_staff):
    def _create_ticket(issue=None):
        if not issue:
            issue = faker.sentence()
        tenant = create_tenant()
        ticket = TicketModel.create(
            schema=TicketSchema,
            payload=ticket_attributes(issue, tenant, create_join_staff()),
        )
        ticket.save_to_db()
        return ticket

    yield _create_ticket
