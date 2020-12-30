import pytest
from models.notes import NotesModel


@pytest.fixture
def note_attributes():
    def _note_attributes(text, user, ticket):
        return {"text": text, "userid": user.id, "ticketid": ticket.id}

    yield _note_attributes


@pytest.fixture
def create_note(faker, note_attributes):
    text = faker.paragraph()

    def _create_note(userid, ticketid, text=text):
        note = NotesModel(**note_attributes(text, userid, ticketid))
        note.save_to_db()
        return note

    yield _create_note
