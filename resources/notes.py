from flask_restful import Resource
from flask import request
from models.notes import NotesModel
from models.tickets import TicketModel
from utils.authorizations import pm_level_required
from schemas.notes import NotesSchema
from flask_jwt_extended import get_jwt_identity


class Note(Resource):
    @pm_level_required
    def post(self, ticket_id):
        TicketModel.find(ticket_id)
        return NotesModel.create(
            schema=NotesSchema,
            payload={
                "text": request.json["text"],
                "ticketid": ticket_id,
                "userid": get_jwt_identity(),
            },
        ).json()

    @pm_level_required
    def delete(self, ticket_id, note_id):
        NotesModel.delete(note_id)
        return {"message": "Note deleted"}
