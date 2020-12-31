import pytest
from tests.unit.base_interface_test import BaseInterfaceTest
from models.notes import NotesModel
from schemas.notes import NotesSchema
from utils.time import Time
from models.user import UserModel

class TestBaseNotesModel(BaseInterfaceTest):
    def setup(self):
        self.object = NotesModel()
        self.custom_404_msg = 'Notes not found'
        self.schema = NotesSchema

@pytest.mark.usefixtures('empty_test_db')
class TestNotesModel():
    def test_json(self, create_note, create_ticket):
        ticket = create_ticket()
        user = UserModel.query.filter_by(id = ticket.senderID).first()
        note = create_note(user, ticket)

        assert note.json() == {
            'id': note.id,
            'ticketid': note.ticketid,
            'text': note.text,
            'user': user.full_name(),
            'created_at': Time.format_date(note.created_at),
            'updated_at': Time.format_date(note.updated_at)
        }
