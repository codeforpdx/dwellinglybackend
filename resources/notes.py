from flask_restful import Resource
from flask import request
from models.notes import NotesModel
from models.tickets import TicketModel
from utils.authorizations import pm_level_required
from schemas.notes import NotesSchema
from flask_jwt_extended import get_jwt_identity


class Notes(Resource):
    @pm_level_required
    def post(self, id):
        TicketModel.find(id)
        return NotesModel.create(
            schema=NotesSchema,
            payload={
                "text": request.json["text"],
                "ticket_id": id,
                "user_id": get_jwt_identity(),
            },
        ).json()

class Note(Resource):
    @pm_level_required

    def delete(self, ticket_id, id):
        ticket = TicketModel.find(ticket_id)
        ticket.notes.delete(NotesModel.find(id))

        return {"message": "Note deleted"}

    @pm_level_required
    def patch(self, ticket_id, note_id):

        return NotesModel.update(
            schema=NotesSchema, id=note_id, payload={"text": request.json["text"]}
        ).json()
