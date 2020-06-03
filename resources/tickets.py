from flask_restful import Resource, reqparse
import json
from models.tickets import TicketModel
from models.notes import NotesModel
from resources.admin_required import admin_required


class Ticket(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('sender')
    parser.add_argument('tenant')
    parser.add_argument('status')
    parser.add_argument('urgency')
    parser.add_argument('issue')
    parser.add_argument('note')

    @admin_required
    def get(self, id):
        ticket= TicketModel.find_by_id(id)
        if ticket:
            return ticket.json()
        return {'message': 'Ticket Not Found'}, 404

    @admin_required
    def delete(self, id):
        ticket= TicketModel.find_by_id(id)
        if ticket:
            ticket.delete_from_db()

        return{'Message': 'Ticket Removed from Database'}

    @admin_required
    def put(self, id):
        data = Ticket.parser.parse_args()
        ticket = TicketModel.find_by_id(id)

        #variable statements allow for only updated fields to be transmitted
        if(data.sender):
            ticket.sender = data.sender

        if(data.tenant):
            ticket.tenant = data.tenant

        if(data.status):
            ticket.status = data.status

        if(data.urgency):
            ticket.urgency = data.urgency

        if(data.issue):
            ticket.issue = data.issue

        if(data.note):
            note = NotesModel(id, data.note, ticket.sender)
            try:
                note.save_to_db()
            except:
                return {'Message': 'An Error Has Occured'}, 500
        try:
            ticket.save_to_db()
        except:
            return{"message": "An error has occured updating the property"}, 500

        return ticket.json()

class Tickets(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('sender')
    parser.add_argument('tenant')
    parser.add_argument('status')
    parser.add_argument('urgency')
    parser.add_argument('issue')

    @admin_required
    def get(self):
        return {'Tickets': [ticket.json() for ticket in TicketModel.query.all()]}

    @admin_required
    def post(self):
        data = Tickets.parser.parse_args()
        ticket = TicketModel(**data)

        try:
            ticket.save_to_db()
        except:
            return {'Message': 'An Error Has Occured'}, 500
        return ticket.json(), 201
