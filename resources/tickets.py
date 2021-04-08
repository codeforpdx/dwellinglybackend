from flask_restful import Resource, reqparse
from models.tickets import TicketModel
from models.notes import NotesModel
from utils.authorizations import pm_level_required


class Ticket(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("senderID")
    parser.add_argument("tenantID")
    parser.add_argument("status")
    parser.add_argument("urgency")
    parser.add_argument("issue")
    parser.add_argument("note")
    parser.add_argument("assignedUserID")

    @pm_level_required
    def get(self, id):
        ticket = TicketModel.find_by_id(id)
        if ticket:
            return ticket.json()
        return {"message": "Ticket not found"}, 404

    @pm_level_required
    def delete(self, id):
        ticket = TicketModel.find_by_id(id)
        if ticket:
            ticket.delete_from_db()
            return {"message": "Ticket removed from database"}
        return {"message": "Ticket not found"}, 404

    @pm_level_required
    def put(self, id):
        data = Ticket.parser.parse_args()
        ticket = TicketModel.find_by_id(id)

        if ticket:
            # variable statements allow for only updated fields to be transmitted
            if data.senderID:
                ticket.senderID = data.senderID

            if data.tenantID:
                ticket.tenantID = data.tenantID

            if data.assignedUserID:
                ticket.assignedUserID = data.assignedUserID

            if data.status:
                ticket.status = data.status

            if data.urgency:
                ticket.urgency = data.urgency

            if data.issue:
                ticket.issue = data.issue

            if data.note:
                note = NotesModel(ticketid=id, text=data.note, userid=ticket.senderID)
                note.save_to_db()

            ticket.save_to_db()
            return ticket.json()
        return {"message": "Ticket not found"}, 404


class Tickets(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("senderID")
    parser.add_argument("tenantID")
    parser.add_argument("status")
    parser.add_argument("urgency")
    parser.add_argument("issue")
    parser.add_argument("assignedUserID")

    @pm_level_required
    def get(self):
        data = Tickets.parser.parse_args()
        if data["tenantID"]:
            return {
                "tickets": [
                    ticket.json()
                    for ticket in TicketModel.find_by_tenantID(data["tenantID"])
                ]
            }
        else:
            return {"tickets": [ticket.json() for ticket in TicketModel.query.all()]}

    @pm_level_required
    def post(self):
        data = Tickets.parser.parse_args()
        ticket = TicketModel(**data)

        ticket.save_to_db()
        return ticket.json(), 201

    @pm_level_required
    def delete(self):
        self.parser.add_argument("ids", action="append")
        data = Tickets.parser.parse_args()

        if not ("ids" in data and type(data["ids"]) is list):
            return {"message": "Ticket IDs missing in request"}, 400

        for id in data["ids"]:
            ticket = TicketModel.find(id)
            if not ticket:
                continue
            ticket.delete_from_db()

        return {"message": "Tickets successfully deleted"}, 200
