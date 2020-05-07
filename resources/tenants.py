import json
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_claims
from db import db
from models.tenant import TenantModel

# | method | route                | action                    |
# | :----- | :------------------- | :------------------------ |
# | GET    | `v1/tenants/`        | Gets all tenants          |
# | POST   | `v1/tenants/`        | Creates a new tenant      |

class Tenants(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('firstName',type=str,required=True,help="This field cannot be blank.")
    parser.add_argument('lastName',type=str,required=True,help="This field cannot be blank.")
    parser.add_argument('phone',type=str,required=True,help="This field cannot be blank.")
    parser.add_argument('propertyID',required=False,help="This field can be provided at a later time.")
    
    def get(self):
        return {'tenants': [tenant.json() for tenant in TenantModel.query.all()]}

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
