import pytest
from conftest import is_valid
from models.notes import NotesModel

newNote = {"text": "We don't need no water"}


@pytest.mark.usefixtures("client_class", "empty_test_db")
class TestCreate:
    def setup(self):
        self.endpoint = "/api/tickets"

    def test_it_returns_the_created_note(
        self, valid_header, create_admin_user, create_tenant, create_ticket
    ):
        create_admin_user()
        create_tenant()
        validTicketID = create_ticket().json()["id"]

        response = self.client.post(
            f"{self.endpoint}/{validTicketID}/notes", json=newNote, headers=valid_header
        )
        createdNote = NotesModel.find(response.json["id"])

        assert response.json == createdNote.json()

    def test_it_returns_404_with_invalid_ticket(self, valid_header):
        invalidTicketID = 777

        response = self.client.post(
            f"{self.endpoint}/{invalidTicketID}/notes",
            json=newNote,
            headers=valid_header,
        )
        assert is_valid(response, 404)  # Bad Request- 'Invalid Ticket'
