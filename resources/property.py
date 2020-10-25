import json
from flask_restful import Resource, reqparse
from resources.admin_required import admin_required
from db import db
from models.property import PropertyModel
from models.user import UserModel

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
    parser.add_argument('unit')
    parser.add_argument('city')
    parser.add_argument('zipcode')
    parser.add_argument('state')
    parser.add_argument('propertyManagerIDs')
    parser.add_argument('archived')

    def get(self):
        return {'properties': [property.json() for property in db.session.query(PropertyModel).all()]}

    @admin_required
    def post(self):
        data = Properties.parser.parse_args()

        if PropertyModel.find_by_name(data["name"]):
            return { 'message': 'A property with this name already exists'}, 401

        rentalproperty = PropertyModel(**data)

        PropertyModel.save_to_db(rentalproperty)

        return rentalproperty.json(), 201

class ArchiveProperty(Resource):

    @admin_required
    def post(self, id):
        property = PropertyModel.find_by_id(id)
        if(not property):
            return{'message': 'Property cannot be archived'}, 400

        property.archived = not property.archived

        property.save_to_db()

        return property.json(), 201

# single property/name
class Property(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name')
    parser.add_argument('address')
    parser.add_argument('unit')
    parser.add_argument('city')
    parser.add_argument('zipcode')
    parser.add_argument('state')
    parser.add_argument('propertyManagerIDs')
    parser.add_argument('tenants')
    parser.add_argument('archived')

    @admin_required
    def get(self, name):
        rentalProperty = PropertyModel.find_by_name(name)

        if rentalProperty:
            return rentalProperty.json()
        return {'message': 'Property not found'}, 404

    @admin_required
    def delete(self, name):
        property = PropertyModel.find_by_name(name)
        if property:
            property.delete_from_db()
            return {'message': 'Property deleted'}
        return {'message': 'Property not found'}, 404

    @admin_required
    def put(self, name):
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

        if data.propertyManagerIDs:
            rentalProperty.managers = PropertyModel.set_property_managers(data.propertyManagerIDs)

        #the reported purpose of this route is toggling the "archived" status
        #but an explicit value of "archive" in the request body will override
        rentalProperty.archived = not rentalProperty.archived
        if(data.archived == True or data.archived == False):
            rentalProperty.archived = data.archived

        rentalProperty.save_to_db()

        return rentalProperty.json()
