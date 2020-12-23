from flask import request
from flask_restful import Resource
from models.lease import LeaseModel
from schemas.lease import LeaseSchema
from serializers.lease import LeaseSerializer
from utils.time import time_format
from utils.authorizations import pm_level_required


class Lease(Resource):
    @pm_level_required
    def get(self, id):
        return LeaseSerializer.serialize(
            LeaseModel.find(id)
        )

    @pm_level_required
    def put(self,id):
        return LeaseSerializer.serialize(
            LeaseModel.update(
                schema=LeaseSchema,
                id=id,
                payload=request.json)
        )

    @pm_level_required
    def delete(self, id):
        LeaseModel.delete(id)
        return {'message': 'Lease deleted'}

class Leases(Resource):
    @pm_level_required
    def get(self):
        return {'leases': LeaseSerializer.serialize(
                LeaseModel.query.all(), many=True
            )
        }

    @pm_level_required
    def post(self):
        LeaseModel.create(
            schema=LeaseSchema,
            payload=request.json
        )
        return {'message': 'Lease created successfully'}, 201
