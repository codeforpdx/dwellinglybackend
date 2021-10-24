import pytest
from models.tickets import TicketModel
from utils.time import TimeStamp


@pytest.mark.usefixtures("client_class", "empty_test_db")
class TestWidgets:
    def test_get_widgets(self, valid_header, create_ticket):
        def _create_tickets(num, status):
            for _ in range(num):
                create_ticket(status=status)

        def _create_tickets_more_than_week_old(num, status):
            for _ in range(num):
                create_ticket(status=status, updated_at=TimeStamp.weeks_ago(2))

        _create_tickets(2, TicketModel.NEW)
        _create_tickets(3, TicketModel.IN_PROGRESS)
        _create_tickets_more_than_week_old(5, TicketModel.NEW)
        _create_tickets_more_than_week_old(7, TicketModel.IN_PROGRESS)

        widget_response = self.client.get("/api/widgets", headers=valid_header)

        assert widget_response.status_code == 200
        assert widget_response.json == {
            "managers": [],
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
