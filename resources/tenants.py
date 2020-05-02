import json
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_claims
from db import db
from models.tenant import TenantModel

# | method | route                | action                    |
# | :----- | :------------------- | :------------------------ |
# | GET    | `v1/tenants/`        | Gets all tenants          |
# | POST   | `v1/tenants/`        | Creates a new tenant      |
# | GET    | `v1/tenants/:id`     | Gets a single tenant      |
# | PUT    | `v1/tenants/:id`     | Updates a single tenant   |
# | DELETE | `v1/tenants/:id`     | Deletes a single tenant   |

class Tenants(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('firstName',type=str,required=True,help="This field cannot be blank.")
    parser.add_argument('lastName',type=str,required=True,help="This field cannot be blank.")
    parser.add_argument('phone',type=str,required=True,help="This field cannot be blank.")
    parser.add_argument('propertyID',required=False,help="This field can be provided at a later time.")
    
    
    def get(self, tenant_id=None):
        # The get all endpoint is useful for development. Disable before production??
        if not tenant_id:
            return {'tenants': [tenant.json() for tenant in TenantModel.query.all()]}

        tenant = TenantModel.find_by_id(tenant_id)
        
        if not tenant:
            return {'message': 'Tenant not found'}, 404
        return tenant.json()


    @jwt_required
    def post(self):
        #check if is_admin exist if not discontinue function
        claims = get_jwt_claims() 
        
        if not claims['is_admin']:
            return {'message': "Admin Access Required"}, 401

        data = Tenants.parser.parse_args()

        if TenantModel.find_by_first_and_last(data["firstName"], data["lastName"]):
            return { 'message': 'A tenant with this first and last name already exists'}, 401

        tenantEntry = TenantModel(**data) 

        try:
            TenantModel.save_to_db(tenantEntry)
        except:
            return{"Message": "An Internal Error has Occured. Unable to insert tenant"}, 500

        return tenantEntry.json(), 201


    @jwt_required
    def put(self, tenant_id):

        claims = get_jwt_claims() 

        if not claims['is_admin']:
            return {'message': "Admin Access Required"}, 401

        parser_for_put = Tenants.parser.copy()
        parser_for_put.replace_argument('firstName',required=False)
        parser_for_put.replace_argument('lastName',required=False)
        parser_for_put.replace_argument('phone',required=False)
        parser_for_put.replace_argument('propertyID',required=False)
        data = parser_for_put.parse_args()

        tenantEntry = TenantModel.find_by_id(tenant_id)
        if not tenantEntry:
            return {'message': 'Tenant not found.'}, 404

        #variable statements allow for only updated fields to be transmitted 
        if(data.firstName):
            tenantEntry.firstName = data.firstName
            
        if(data.lastName):
            tenantEntry.lastName = data.lastName

        if(data.phone):
            tenantEntry.phone = data.phone
        
        if(data.propertyID):
            tenantEntry.propertyID = data.propertyID
        
        try:
            tenantEntry.save_to_db()
        except:
            return{"message": "An error has occured updating the tenant"}, 500

        return tenantEntry.json()


    @jwt_required
    def delete(self, tenant_id):
        claims = get_jwt_claims() 

        if not claims['is_admin']:
            return {'message': "Admin Access Required"}, 401

        tenant = TenantModel.find_by_id(tenant_id)
        if not tenant:
            return {'message': 'Tenant not found.'}, 404

        tenant.delete_from_db()
        return {'message': 'Tenant deleted.'}

