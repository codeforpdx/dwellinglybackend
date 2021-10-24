import pytest
from models.tickets import TicketModel
from utils.time import TimeStamp


@pytest.mark.usefixtures("client_class", "empty_test_db")
class TestWidgets:
    def test_get_widgets(self, valid_header, create_ticket, create_property_manager, create_property):
        response = self.client.get("/api/widgets", headers=valid_header)

        assert response.status_code == 200
