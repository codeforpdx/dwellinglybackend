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
        ticket= TicketModel.find_by_id(id)
        if ticket:
            return ticket.json()
        return {'message': 'Ticket Not Found'}, 404

    @jwt_required
    def delete(self, id):
        ticket= TicketModel.find_by_id(id)
        if ticket:
            ticket.delete_from_db()

        return {'Message': 'Ticket Removed from Database'}

    @jwt_required
    def put(self, id):
        data = Ticket.parser.parse_args()
        ticket = TicketModel.find_by_id(id)
        updated = False
        dateTime = datetime.now()

        if ticket:
            #variable statements allow for only updated fields to be transmitted
            if(data.sender):
                ticket.sender = data.sender
                updated = True

            if(data.tenant):
                ticket.tenant = data.tenant
                updated = True

            if(data.assignedUser):
                ticket.assignedUser = data.assignedUser
                updated = True

            if(data.status):
                ticket.status = data.status
                updated = True

            if(data.urgency):
                ticket.urgency = data.urgency
                updated = True

            if(data.issue):
                ticket.issue = data.issue
                updated = True

            if(data.note):
                note = NotesModel(id, data.note, ticket.sender)
                updated = True
                try:
                    note.save_to_db()
                except:
                    return {'Message': 'An Error Has Occured'}, 500

            if updated:
                timestamp = dateTime.strftime("%d-%b-%Y (%H:%M)")
                ticket.updated = timestamp

            try:
                ticket.save_to_db()
            except:
                return{"message": "An error has occured updating the Ticket"}, 500

            return ticket.json()

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
        return {'Tickets': [ticket.json() for ticket in TicketModel.query.all()]}

    @jwt_required
    def post(self):
        data = Tickets.parser.parse_args()
        ticket = TicketModel(**data)

        try:
            ticket.save_to_db()
        except:
            return {'Message': 'An Error Has Occured'}, 500
        return ticket.json(), 201
