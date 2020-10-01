from flask_restful import Resource, reqparse
import json
from models.tickets import TicketModel
from models.notes import NotesModel
from flask_jwt_extended import jwt_required
from datetime import datetime

class Ticket(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('sender')
    parser.add_argument('tenant')
    parser.add_argument('status')
    parser.add_argument('urgency')
    parser.add_argument('issue')
    parser.add_argument('note')
    parser.add_argument('assignedUser')


    @jwt_required
    def get(self, id):
        ticket = TicketModel.find_by_id(id)
        if ticket:
            return ticket.json()
        return {'message': 'Ticket not found'}, 404

    @jwt_required
    def delete(self, id):
        ticket = TicketModel.find_by_id(id)
        if ticket:
            ticket.delete_from_db()
            return {'message': 'Ticket removed from database'}
        return {'message': 'Ticket not found'}, 404

    @jwt_required
    def put(self, id):
        data = Ticket.parser.parse_args()
        ticket = TicketModel.find_by_id(id)

        if ticket:
            #variable statements allow for only updated fields to be transmitted
            if(data.sender):
                ticket.sender = data.sender

            if(data.tenant):
                ticket.tenant = data.tenant

            if(data.assignedUser):
                ticket.assignedUser = data.assignedUser

            if(data.status):
                updated = not (ticket.status == data.status)
                if updated:
                    ticket.status = data.status
                    ticket.updated = datetime.now()

            if(data.urgency):
                ticket.urgency = data.urgency

            if(data.issue):
                ticket.issue = data.issue

            if(data.note):
                note = NotesModel(id, data.note, ticket.sender)
                try:
                    note.save_to_db()
                except:
                    return {'message': 'An error has occured'}, 500

            try:
                ticket.save_to_db()
            except:
                return{"message": "An error has occured updating the ticket"}, 500

            return ticket.json()
        return {'message': 'Ticket not found'}, 404

class Tickets(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('sender')
    parser.add_argument('tenant')
    parser.add_argument('status')
    parser.add_argument('urgency')
    parser.add_argument('issue')
    parser.add_argument('assignedUser')

    @jwt_required
    def get(self):
        data = Tickets.parser.parse_args()
        if data["tenant"]:
            return {'tickets': [ticket.json() for ticket in TicketModel.find_by_tenantID(data["tenant"])]}
        else:
            return {'tickets': [ticket.json() for ticket in TicketModel.query.all()]}

    @jwt_required
    def post(self):
        data = Tickets.parser.parse_args()
        ticket = TicketModel(**data)

        try:
            ticket.save_to_db()
        except:
            return {'message': 'An error has occured'}, 500
        return ticket.json(), 201
