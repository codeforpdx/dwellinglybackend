from flask_restful import Resource
from flask import request
from utils.authorizations import admin_required
from models.tenant import TenantModel
from models.lease import LeaseModel
from schemas.lease import LeaseSchema
from schemas.tenant import TenantSchema


class Tenant(Resource):
    @admin_required
    def get(self, id):
        return TenantModel.find(id).json()

    @admin_required
    def put(self, id):
        return TenantModel.update(
            schema=TenantSchema, payload=request.json, id=id
        ).json()


class Tenants(Resource):
    @admin_required
    def get(self):
        return {"tenants": TenantModel.query.json()}

    @admin_required
    def post(self):
        tenantEntry = TenantModel.create(schema=TenantSchema, payload=request.json)

        returnData = tenantEntry.json()

        leaseData = request.json
        leaseData.update({"tenantID": tenantEntry.id})

        def _lease():
            return (
                "dateTimeEnd" in leaseData
                and "dateTimeStart" in leaseData
                and "propertyID" in leaseData
            )

        if _lease():
            LeaseModel.create(schema=LeaseSchema, payload=leaseData)
            returnData.update(
                {
                    "occupants": leaseData["occupants"],
                    "propertyID": leaseData["propertyID"],
                    "unitNum": leaseData["unitNum"],
                }
            )

        return returnData, 201
