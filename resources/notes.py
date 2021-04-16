from flask_restful import Resource, reqparse
from models.notes import NotesModel
from utils.authorizations import pm_level_required
from schemas.notes import NotesSchema


class Notes(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("text")
    parser.add_argument("authorID")

    @pm_level_required
    def post(self, id):
        data = Notes.parser.parse_args()
        note_payload = {"ticketid": id, "text": data.text, "userid": data.authorID}

        created_note = NotesModel.create(schema=NotesSchema, payload=note_payload)
        return created_note.json()
