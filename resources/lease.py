from flask import request
from flask_restful import Resource
from models.lease import LeaseModel
from schemas.lease import LeaseSchema
from flask_jwt_extended import jwt_required


class Lease(Resource):
    @jwt_required
    def get(self, id):
        return LeaseModel.find(id).json()

    @jwt_required
    def put(self,id):
        return LeaseModel.update(LeaseSchema(), id, request.json).json()

    @jwt_required
    def delete(self, id):
        LeaseModel.delete(id)
        return {'message': 'Lease deleted'}

class Leases(Resource):
    @jwt_required
    def get(self):
        return {'Leases': [lease.json() for lease in LeaseModel.query.all()]}

    @jwt_required
    def post(self):
        LeaseModel.create(LeaseSchema(), request.json)
        return {'message': 'Lease created successfully'}, 201
