from flask_restful import Resource, reqparse
from models.tickets import TicketModel
from models.tenant import TenantModel
from utils.authorizations import pm_level_required
from flask import request


class Ticket(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("senderID")
    parser.add_argument("tenantID")
    parser.add_argument("status")
    parser.add_argument("urgency")
    parser.add_argument("issue")
    parser.add_argument("assignedUserID")

    @pm_level_required
    def get(self, id):
        return TicketModel.find(id).json()

    @pm_level_required
    def delete(self, id):
        ticket = TicketModel.find(id)
        ticket.delete_from_db()
        return {"message": "Ticket removed from database"}

    @pm_level_required
    def put(self, id):
        data = Ticket.parser.parse_args()
        ticket = TicketModel.find(id)

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

        ticket.save_to_db()
        return ticket.json()


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
            return {"tickets": TenantModel.find(data["tenantID"]).tickets.json()}
        else:
            return {"tickets": TicketModel.query.json()}

    @pm_level_required
    def post(self):
        data = Tickets.parser.parse_args()
        ticket = TicketModel(**data)

        ticket.save_to_db()
        return ticket.json(), 201

    @pm_level_required
    def delete(self):
        data = request.json

        if not ("ids" in data and type(data["ids"]) is list):
            return {"message": "Ticket IDs missing in request"}, 400

        TicketModel.query.filter(TicketModel.id.in_(data["ids"])).delete(
            synchronize_session="fetch"
        )

        return {"message": "Tickets successfully deleted"}, 200
