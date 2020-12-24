import json
from flask_restful import Resource, reqparse
from flask import request
from utils.authorizations import admin_required
from db import db
from models.tenant import TenantModel
from models.user import UserModel
from models.lease import LeaseModel
from schemas.lease import LeaseSchema
from schemas.tenant import TenantSchema
from datetime import datetime
from utils.time import Time
from schemas.lease import LeaseSchema
from datetime import datetime

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
            return {'tenants': [tenant.json() for tenant in TenantModel.query.all()]}

        # GET /tenants/<tenant_id>
        tenant = TenantModel.find_by_id(tenant_id)
        if not tenant:
            return {'message': 'Tenant not found'}, 404
        return tenant.json()


    @admin_required
    def post(self):
        tenantEntry = TenantModel.create(schema=TenantSchema, payload=request.json)

        returnData = tenantEntry.json()

        leaseData = request.json
        leaseData.update({'tenantID': tenantEntry.id})

        #if this tenant has a lease
        if ("dateTimeEnd" in leaseData and "dateTimeStart" in leaseData and "propertyID" in leaseData):
            LeaseModel.create(
                schema=LeaseSchema,
                payload=leaseData
            )
            returnData.update({'occupants': leaseData['occupants'], 'propertyID': leaseData['propertyID'], 'unitNum': leaseData['unitNum']})

        return returnData, 201


    @admin_required
    def put(self, tenant_id):
        return TenantModel.update(schema=TenantSchema, payload=request.json, id=tenant_id).json()

    @admin_required
    def delete(self, tenant_id):
        tenant = TenantModel.find_by_id(tenant_id)
        if not tenant:
            return {'message': 'Tenant not found'}, 404

        tenant.delete_from_db()
        return {'message': 'Tenant deleted'}
