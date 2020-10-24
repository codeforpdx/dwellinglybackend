from flask import request
from flask_restful import Resource
from models.lease import LeaseModel
from schemas.lease import LeaseSchema
from serializers.lease import LeaseSerializer
from flask_jwt_extended import jwt_required
from utils.time import time_format


class Lease(Resource):
    @jwt_required
    def get(self, id):
        return LeaseSerializer.serialize(
            LeaseModel.find(id)
        )

    @jwt_required
    def put(self,id):
        return LeaseSerializer.serialize(
            LeaseModel.update(
                schema=LeaseSchema,
                id=id,
                payload=request.json)
        )

    @jwt_required
    def delete(self, id):
        LeaseModel.delete(id)
        return {'message': 'Lease deleted'}

class Leases(Resource):
    @jwt_required
    def get(self):
        return {'leases': LeaseSerializer.serialize(
                LeaseModel.query.all(), many=True
            )
        }

    @jwt_required
    def post(self):
        LeaseModel.create(
            schema=LeaseSchema,
            payload=request.json
        )
        return {'message': 'Lease created successfully'}, 201
