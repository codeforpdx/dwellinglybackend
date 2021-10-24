import pytest

from models.tickets import TicketModel
from utils.time import TimeStamp
from models.dashboard import Dashboard


@pytest.mark.usefixtures("empty_test_db")
class TestDashboard:
    def test_json(self, valid_header, create_ticket, create_property_manager, create_property):
        def _create_tickets(num, status, updated_at=None):
            updated_at = updated_at or TimeStamp.now()
            for _ in range(num):
                create_ticket(status=status, updated_at=updated_at)

        _create_tickets(2, TicketModel.NEW)
        _create_tickets(5, TicketModel.NEW, TimeStamp.weeks_ago(1))
        _create_tickets(3, TicketModel.IN_PROGRESS)
        _create_tickets(7, TicketModel.IN_PROGRESS, TimeStamp.weeks_ago(2))

        pm = create_property_manager()
        pm2 = create_property_manager(created_at=TimeStamp.days_ago(1))
        pm3 = create_property_manager(created_at=TimeStamp.days_ago(2))
        prop = create_property(manager_ids=[pm.id])
        prop2 = create_property(manager_ids=[pm.id, pm3.id])

        response = Dashboard.json()

        assert response == {
            "managers": [
                {
                    "date": "Today",
                    "firstName": pm.firstName,
                    "id": pm.id,
                    "lastName": pm.lastName,
                    "propertyName": prop.name
                },
                {
                    "date": "Yesterday",
                    "firstName": pm2.firstName,
                    "id": pm2.id,
                    "lastName": pm2.lastName,
                    "propertyName": "Not Assigned"
                },
                {
                    "date": "This Week",
                    "firstName": pm3.firstName,
                    "id": pm3.id,
                    "lastName": pm3.lastName,
                    "propertyName": prop2.name
                },
            ],
            "opentickets": {
                "new": {
                    "allNew": {
                        "stat": 7,
                        "desc": "New",
                    },
                    "unseen24Hrs": {
                        "stat": 2,
                        "desc": "Unseen for > 24 hours",
                    },
                },
                "inProgress": {
                    "allInProgress": {
                        "stat": 10,
                        "desc": "In Progress",
                    },
                    "inProgress1Week": {
                        "stat": 3,
                        "desc": "In progress for > 1 week",
                    },
                },
            },
        }
