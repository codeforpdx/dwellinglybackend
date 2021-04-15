from flask_restful import Resource, reqparse
from models.notes import NotesModel
from models.tickets import TicketModel
from utils.authorizations import pm_level_required


class Note(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("text")
    parser.add_argument("authorID")

    @pm_level_required
    def post(self, id):
        data = Note.parser.parse_args()
        note = NotesModel(ticketid=id, text=data.text, userid=data.authorID)
        note.save_to_db()

        ticket = TicketModel.find(id)
        return ticket.json()
