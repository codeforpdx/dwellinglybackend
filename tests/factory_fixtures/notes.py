import pytest
from models.notes import NotesModel
from schemas.notes import NotesSchema
from tests.attributes import note_attrs


@pytest.fixture
def note_attributes(faker):
    def _note_attributes(text, user, ticket):
        return {**note_attrs(faker, text), "user_id": user.id, "ticket_id": ticket.id}

    yield _note_attributes


@pytest.fixture
def create_note(faker, note_attributes, create_admin_user, create_ticket):
    def _create_note(user=None, ticket=None, text=None):
        user = user or create_admin_user()
        ticket = ticket or create_ticket()

        return NotesModel.create(
            schema=NotesSchema, payload=note_attributes(text, user, ticket)
        )

    yield _create_note
