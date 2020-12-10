import pytest
from models.notes import NotesModel

@pytest.fixture
def note_attributes():
    def _note_attributes(text, user, ticket):
        return {
            'text': text,
            'user': user.id,
            'ticketid': ticket.id
        }
    yield _note_attributes

@pytest.fixture
def create_note(note_attributes, create_join_staff):
    class SimpleTicket:
        def __init__(self, id):
            self.id = id

    class SimpleUser:
        def __init__(self, id):
            self.id = id

    def _create_note(user=SimpleUser(1),
                     text="This is a note",
                     ticket=SimpleTicket(1)):
        note = NotesModel(**note_attributes(text, user, ticket))
        note.save_to_db()
        return note
    yield _create_note

