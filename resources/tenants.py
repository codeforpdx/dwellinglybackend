from flask_restful import Resource
from flask import request
from utils.authorizations import admin_required
from models.tenant import TenantModel
from models.lease import LeaseModel
from schemas.lease import LeaseSchema
from schemas.tenant import TenantSchema

# | method | route                | action                    |
# | :----- | :------------------- | :------------------------ |
# | POST   | `v1/tenants/`        | Creates a new tenant      |
# | GET    | `v1/tenants/`        | Gets all tenants          |
# | GET    | `v1/tenants/:id`     | Gets a single tenant      |
# | PUT    | `v1/tenants/:id`     | Updates a single tenant   |
# | DELETE | `v1/tenants/:id`     | Deletes a single tenant   |


class Tenants(Resource):
    @admin_required
    def get(self, tenant_id=None):
        # GET /tenants
        if not tenant_id:
            return {"tenants": [tenant.json() for tenant in TenantModel.query.all()]}

        # GET /tenants/<tenant_id>
        return TenantModel.find(tenant_id).json()

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

    @admin_required
    def put(self, tenant_id):
        return TenantModel.update(
            schema=TenantSchema, payload=request.json, id=tenant_id
        ).json()
