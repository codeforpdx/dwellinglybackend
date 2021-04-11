import pytest
from schemas.notes import NotesSchema
from models.user import UserModel


class TestNotesSchemaSerialization:
    @pytest.mark.usefixtures("empty_test_db")
    def test_notes_serialization(self, create_note, create_ticket):
        ticket = create_ticket()
        user = UserModel.query.filter_by(id=ticket.senderID).first()
        note = create_note(user, ticket)

        note_schema = NotesSchema()
        note_json = note_schema.dump(note)
        assert note_json["text"] == note.text
        assert note_json["user"] == "%s %s" % (user.firstName, user.lastName)
        assert "userinfo" not in note_json

    @pytest.mark.usefixtures("empty_test_db")
    def test_notes_user_validation(self, create_ticket):
        note_schema = NotesSchema(exclude=["user"])
        ticket = create_ticket()
        payload = {"userid": 500, "text": "Invalid User ID", "ticketid": ticket.id}
        validation_errors = note_schema.validate(payload)
        assert "userid" in validation_errors
        assert validation_errors["userid"] == ["500 is not a valid User ID"]

    @pytest.mark.usefixtures("empty_test_db")
    def test_notes_ticket_validation(self, create_join_staff):
        note_schema = NotesSchema(exclude=["user"])
        user = create_join_staff()
        payload = {"userid": user.id, "text": "Invalid Ticket ID", "ticketid": 500}

        validation_errors = note_schema.validate(payload)
        assert "ticketid" in validation_errors
        assert validation_errors["ticketid"] == ["500 is not a valid Ticket ID"]
