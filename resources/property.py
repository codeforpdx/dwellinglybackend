from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_claims
from db import db
from models.property import PropertyModel

# | method | route                | action                     |
# | :----- | :------------------- | :------------------------- |
# | POST   | `v1/properties/`     | Creates a new property     |
# | GET    | `v1/properties/`   | Gets all properties        |
# | GET    | `v1/property/:name`  | Gets a single property     |
# | PUT    | `v1/property/:name`  | Updates a single property  |
# | DELETE | `v1/property/:name`  | Deletes a single property  |

#TODO Add Id based identifiers. 
#TODO Incorporate JWT Claims for Admin 

class Properties(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name')
    parser.add_argument('address') 
    parser.add_argument('city')
    parser.add_argument('zipcode')
    parser.add_argument('state')
    parser.add_argument('archived')
    
    def get(self):
        return {'properties': [property.json() for property in PropertyModel.query.all()]}
    
    @jwt_required
    def post(self):
        #check if is_admin exist if not discontinue function
        claims = get_jwt_claims() 
        
        if not claims['is_admin']:
            return {'Message', "Admin Access Required"}, 401

        data = Properties.parser.parse_args()

        if PropertyModel.find_by_name(data["name"]):
            return { 'Message': 'A property with this name already exists'}, 401

        rentalproperty = PropertyModel(**data) 

        try:
            PropertyModel.save_to_db(rentalproperty)
        except:
            return{"Message": "An Internal Error has Occured. Unable to insert Property"}, 500

        return rentalproperty.json(), 201

# single property/name
class Property(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name')
    parser.add_argument('address')
    parser.add_argument('city')
    parser.add_argument('zipcode')
    parser.add_argument('state')
    parser.add_argument('archived')

    @jwt_required
    def get(self, name):
        claims = get_jwt_claims() 

        if not claims['is_admin']:
            return {'Message', "Admin Access Required"}, 401

        rentalProperty = PropertyModel.find_by_name(name)

        if rentalProperty:
            return rentalProperty.json()
        return {'message': 'Property not found'}, 404
    
    @jwt_required
    def delete(self, name):
        claims = get_jwt_claims() 

        if not claims['is_admin']:
            return {'Message', "Admin Access Required"}, 401

        property = PropertyModel.find_by_name(name)
        if property:
            property.delete_from_db()
            return {'message': 'Property deleted.'}
        return {'message': 'Property not found.'}, 404

    @jwt_required
    def put(self, name):

        claims = get_jwt_claims() 

        if not claims['is_admin']:
            return {'Message', "Admin Access Required"}, 401

        data = Properties.parser.parse_args()
        rentalProperty = PropertyModel.find_by_name(name)

        #variable statements allow for only updated fields to be transmitted 
        if(data.address):
            rentalProperty.address = data.address
            
        if(data.city):
            rentalProperty.city = data.city

        if(data.name):
            rentalProperty.name = data.name
        
        if(data.zipcode):
            rentalProperty.zipcode = data.zipcode
        
        if(data.state):
            rentalProperty.state = data.state
        
        #the reported purpose of this route is toggling the "archived" status
        #but an explicit value of "archive" in the request body will override
        rentalProperty.archived = not rentalProperty.archived
        if(data.archived == True or data.archived == False):
            rentalProperty.archived = data.archived
        
        try:
            rentalProperty.save_to_db()
        except:
            return{"message": "An error has occured updating the property"}, 500

        return rentalProperty.json()
    
