from db import db
from flask_restful import Resource
from models.tickets import TicketModel
from utils.authorizations import pm_level_required
from flask import request
from schemas.ticket import TicketSchema


class Ticket(Resource):
    @pm_level_required
    def get(self, id):
        return TicketModel.find(id).json()

    @pm_level_required
    def delete(self, id):
        TicketModel.delete(id)
        return {"message": "Ticket removed from database"}

    @pm_level_required
    def put(self, id):
        ticket = TicketModel.find(id)
        return ticket.update(schema=TicketSchema, payload=request.json).json()


class Tickets(Resource):
    @pm_level_required
    def get(self):
        tickets = TicketModel.query
        if "tenant_id" in request.args:
            tickets = tickets.where(TicketModel.tenant_id == request.args["tenant_id"])
        return {"tickets": tickets.json()}

    @pm_level_required
    def post(self):
        TicketModel.create(schema=TicketSchema, payload=request.json)
        return {"message": "Ticket successfully created"}, 201

    @pm_level_required
    def delete(self):
        data = request.json

        if not ("ids" in data and type(data["ids"]) is list):
            return {"message": "Ticket IDs missing in request"}, 400

        TicketModel.query.filter(TicketModel.id.in_(data["ids"])).delete(
            synchronize_session="fetch"
        )
        db.session.commit()

        return {"message": "Tickets successfully deleted"}, 200
