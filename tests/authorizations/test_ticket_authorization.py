import pytest
from conftest import is_valid


@pytest.mark.usefixtures("client_class")
class TestTicketAuthorization:
    def setup(self):
        self.endpoint = "/api/tickets"
        self.validID = 1

    def test_tickets_DELETE(self):
        response = self.client.delete(f"{self.endpoint}/{self.validID}")
        # UNAUTHORIZED - Missing Authorization Header
        assert is_valid(response, 401)
        assert response.json == {"message": "Missing authorization header"}
