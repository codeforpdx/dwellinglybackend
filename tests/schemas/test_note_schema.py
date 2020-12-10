import pytest
from schemas.notes import *
from models.notes import NotesModel


@pytest.mark.usefixtures("empty_test_db")
class TestNotesSchemaSerialization:
    def test_notes_serialization(self, create_join_staff, create_note):
        user = create_join_staff()
        note = create_note(user)

        note_schema = NotesSchema(exclude=["userinfo"])
        note_json = note_schema.dump(note)
        assert note_json['text'] == note.text
        assert note_json['user'] == "%s %s" % (user.firstName, user.lastName)
        assert not 'userinfo' in note_json

    def test_notes_deserialization(self, create_join_staff):
        note_schema = NotesSchema()
        user = create_join_staff()
        payload = {'user': user.id,
                   'text': 'Test serialization',
                   'ticketid': 1}
        note = note_schema.load(payload)
        assert payload['user'] == note['user']
        assert payload['text'] == note['text']
        assert payload['ticketid'] == note['ticketid']

    def test_notes_user_validation(self):
        note_schema = NotesSchema(exclude=["userinfo"])
        payload = { 'user': 500,
                    'text': "This should fail",
                    'ticketid': 1
                  }
        validation_errors = note_schema.validate(payload)
        assert 'user' in validation_errors
        assert validation_errors['user'] == ['No such user']


