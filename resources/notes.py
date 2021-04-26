from flask_restful import Resource
from flask import request
from models.notes import NotesModel
from utils.authorizations import pm_level_required
from schemas.notes import NotesSchema
from flask_jwt_extended import get_jwt_identity


class Notes(Resource):
    @pm_level_required
    def post(self, id):
        return NotesModel.create(
            schema=NotesSchema,
            payload={
                "text": request.json["text"],
                "ticketid": id,
                "userid": get_jwt_identity(),
            },
        ).json()
