import json
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_claims
from flask import request
from resources.admin_required import admin_required
from db import db
from models.tenant import TenantModel
from models.user import UserModel
from models.lease import LeaseModel
from schemas.lease import LeaseSchema
from datetime import datetime
from utils.time import Time

# | method | route                | action                    |
# | :----- | :------------------- | :------------------------ |
# | POST   | `v1/tenants/`        | Creates a new tenant      |
# | GET    | `v1/tenants/`        | Gets all tenants          |
# | GET    | `v1/tenants/:id`     | Gets a single tenant      |
# | PUT    | `v1/tenants/:id`     | Updates a single tenant   |
# | DELETE | `v1/tenants/:id`     | Deletes a single tenant   |

class Tenants(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('firstName',type=str,required=True,help="This field cannot be blank")
    parser.add_argument('lastName',type=str,required=True,help="This field cannot be blank")
    parser.add_argument('phone',type=str,required=True,help="This field cannot be blank")
    parser.add_argument('propertyID',required=False,help="This field can be provided at a later time")
    parser.add_argument('staffIDs',action='append',required=False,help="This field can be provided at a later time")



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
        data = Tenants.parser.parse_args()
        if TenantModel.find_by_first_and_last(data["firstName"], data["lastName"]):
            return { 'message': 'A tenant with this first and last name already exists'}, 401

        tenantEntry = TenantModel(**data) 
        TenantModel.save_to_db(tenantEntry)

        returnData = tenantEntry.json()

        leaseData = request.json
        leaseData.update({'tenantID': tenantEntry.id})

        #if this tenant has a lease
        if ("dateTimeEnd" in leaseData and "dateTimeStart" in leaseData and "propertyID" in leaseData):

            #convert dateTimeStart and dateTimeEnd from iso8601 format
            leaseData["dateTimeStart"] = Time.format_date(datetime.fromisoformat(leaseData["dateTimeStart"]))
            leaseData["dateTimeEnd"] = Time.format_date(datetime.fromisoformat(leaseData["dateTimeEnd"]))

            LeaseModel.create(
                schema=LeaseSchema,
                payload=leaseData
            )
            returnData.update({'occupants': leaseData['occupants'], 'propertyID': leaseData['propertyID'], 'unitNum': leaseData['unitNum']})
            
        return returnData, 201


    @admin_required
    def put(self, tenant_id):
        parser_for_put = Tenants.parser.copy()
        parser_for_put.replace_argument('firstName',required=False)
        parser_for_put.replace_argument('lastName',required=False)
        parser_for_put.replace_argument('phone',required=False)
        data = parser_for_put.parse_args()

        tenantEntry = TenantModel.find_by_id(tenant_id)
        if not tenantEntry:
            return {'message': 'Tenant not found'}, 404

        #variable statements allow for only updated fields to be transmitted 
        if(data.firstName):
            tenantEntry.firstName = data.firstName
        if(data.lastName):
            tenantEntry.lastName = data.lastName
        if(data.phone):
            tenantEntry.phone = data.phone
        if(data.propertyID):
            tenantEntry.propertyID = data.propertyID
        if(data.staffIDs and len(data.staffIDs)):
            tenantEntry.staff[:] = []
            for id in data.staffIDs:
                user = UserModel.find_by_id(id)
                if user: tenantEntry.staff.append(user)


        tenantEntry.save_to_db()

        return tenantEntry.json()


    @admin_required
    def delete(self, tenant_id):
        tenant = TenantModel.find_by_id(tenant_id)
        if not tenant:
            return {'message': 'Tenant not found'}, 404

        tenant.delete_from_db()
        return {'message': 'Tenant deleted'}

