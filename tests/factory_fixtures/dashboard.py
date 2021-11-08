import pytest

from models.tickets import TicketModel
from utils.time import TimeStamp


@pytest.fixture
def create_dashboard(
    create_ticket, create_property_manager, create_property, create_unauthorized_user
):
    def _create_dashboard(**kwargs):
        def _create_tickets(num, status, tenant=None, author=None, updated_at=None):
            updated_at = updated_at or TimeStamp.now()
            for _ in range(num):
                create_ticket(
                    status=status, tenant=tenant, author=author, updated_at=updated_at
                )

        dashboard = {}
        ticket = create_ticket(status=TicketModel.NEW)
        tenant = ticket.tenant
        author = ticket.author
        dashboard["tenant"] = tenant
        dashboard["author"] = author
        _create_tickets(1, TicketModel.NEW, tenant, author)
        _create_tickets(5, TicketModel.NEW, tenant, author, TimeStamp.weeks_ago(1))
        _create_tickets(3, TicketModel.IN_PROGRESS, tenant, author)
        _create_tickets(
            7, TicketModel.IN_PROGRESS, tenant, author, TimeStamp.weeks_ago(2)
        )

        dashboard["pending_user"] = create_unauthorized_user()
        pm = create_property_manager()
        pm2 = create_property_manager(created_at=TimeStamp.days_ago(1))
        pm3 = create_property_manager(created_at=TimeStamp.days_ago(2))
        dashboard["pm"] = pm
        dashboard["pm2"] = pm2
        dashboard["pm3"] = pm3
        dashboard["prop"] = create_property(manager_ids=[pm.id])
        dashboard["prop2"] = create_property(manager_ids=[pm.id, pm3.id])

        return dashboard

    yield _create_dashboard
