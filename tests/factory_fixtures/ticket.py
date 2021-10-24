import pytest
from models.tickets import TicketModel
from schemas.ticket import TicketSchema
from tests.attributes import ticket_attrs


@pytest.fixture
def ticket_attributes(faker, create_tenant, create_join_staff):
    def _ticket_attributes(issue=None, status=None, tenant=None, author=None, created_at=None, updated_at=None):
        attrs = {
            **ticket_attrs(faker, issue, status),
            "tenant_id": tenant.id if tenant else create_tenant().id,
            "author_id": author.id if author else create_join_staff().id,
        }
        if created_at:
            attrs["created_at"] = created_at
        if updated_at:
            attrs["updated_at"] = updated_at

        return attrs

    yield _ticket_attributes


@pytest.fixture
def create_ticket(faker, ticket_attributes):
    def _create_ticket(**kwargs):
        ticket = TicketModel.create(
            schema=TicketSchema,
            payload=ticket_attributes(**kwargs),
        )
        ticket.save_to_db()
        return ticket

    yield _create_ticket
