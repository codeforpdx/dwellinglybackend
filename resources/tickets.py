from flask_restful import Resource
from models.tickets import TicketModel
from models.tenant import TenantModel
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
        return TicketModel.update(
            schema=TicketSchema, id=id, payload=request.json
        ).json()


class Tickets(Resource):
    @pm_level_required
    def get(self):
        if request.args and request.args["tenant_id"]:
            return {
                "tickets": TenantModel.find(request.args["tenant_id"]).tickets.json()
            }
        else:
            return {"tickets": TicketModel.query.json()}

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

        return {"message": "Tickets successfully deleted"}, 200
