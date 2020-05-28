from flask_restful import Resource, reqparse
from models.tickets import TicketModel

class Ticket(Resource):
    parser = reqparse.RequestParser()

    def get(self, id):
        ticket= TicketModel.find_by_id(id)
        if ticket:
            return ticket.json()
        return {'message': 'Ticket Not Found'}, 404

    def post(self,id):
        if TicketModel.find_by_id(id):
            return{'message': 'Ticket already exists'}, 400
        ticket = TicketModel(id)
        try:
            ticket.save_to_db()
        except:
            return {'Message': 'An Error Has Occured'}, 500
        return ticket.json(), 201

    def delete(self, id):
        ticket= TicketModel.find_by_id(id)
        if ticket:
            ticket.delete_from_db()

        return{'Message': 'Ticket Removed from Database'}

class Tickets(Resource):
    def get(self):
        return {'Tickets': [ticket.json() for ticket in TicketModel.query.all()]}

    def post(self):
        if TicketModel.find_by_id(id):
            return{'message': 'Ticket already exists'}, 400
        ticket = TicketModel(id)
        try:
            ticket.save_to_db()
        except:
            return {'Message': 'An Error Has Occured'}, 500
        return ticket.json(), 201
