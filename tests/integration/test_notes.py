import pytest
from conftest import is_valid
from unittest.mock import patch


@pytest.mark.usefixtures("client_class", "empty_test_db")
class TestCreate:
    def setup(self):
        self.endpoint = "/api/tickets"
        self.new_note = {"text": "We don't need no water"}

    def test_creates_note_through_endpoint(self, valid_header, create_ticket):
        ticket = create_ticket()

        response = self.client.post(
            f"{self.endpoint}/{ticket.id}/notes",
            json=self.new_note,
            headers=valid_header,
        )
        assert response.json == ticket.notes[-1].json()

    def test_it_returns_404_with_invalid_ticket(self, valid_header):
        invalid_ticket_id = 777

        response = self.client.post(
            f"{self.endpoint}/{invalid_ticket_id}/notes",
            json=self.new_note,
            headers=valid_header,
        )

        assert is_valid(response, 404)  # Bad Request- 'Invalid Ticket'


@pytest.mark.usefixtures("client_class", "empty_test_db")
class TestDelete:
    def setup(self):
        self.endpoint = "/api/tickets"

    def test_it_deletes_one_note(
        self, valid_header, create_note, create_admin_user, create_ticket
    ):
        note = create_note()
        ticket = note.ticket

        with patch.object(ticket.notes, "delete") as mock_delete:
            response = self.client.delete(
                f"{self.endpoint}/{note.ticket_id}/notes/{note.id}",
                headers=valid_header,
            )
        mock_delete.assert_called_once_with(note)
        assert response.status_code == 200
        assert response.json == {"message": "Note deleted"}
