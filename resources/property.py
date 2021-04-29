from flask_restful import Resource, reqparse
from flask import request
from utils.authorizations import admin_required
from db import db
from models.property import PropertyModel
from schemas.property import PropertySchema

# | method | route                | action                     |
# | :----- | :------------------- | :------------------------- |
# | POST   | `v1/properties/`     | Creates a new property     |
# | GET    | `v1/properties/`     | Gets all properties        |
# | GET    | `v1/property/:id`    | Gets a single property     |
# | PUT    | `v1/property/:id`    | Updates a single property  |
# | DELETE | `v1/property/:id`    | Deletes a single property  |

# TODO Incorporate JWT Claims for Admin


class Properties(Resource):
    def get(self):
        return {
            "properties": [
                property.json() for property in db.session.query(PropertyModel).all()
            ]
        }

    @admin_required
    def post(self):
        return (
            PropertyModel.create(schema=PropertySchema, payload=request.json).json(),
            201,
        )


class ArchiveProperty(Resource):
    @admin_required
    def post(self, id):
        property = PropertyModel.find(id)

        property.archived = not property.archived

        property.save_to_db()
        message = (
            "Property archived successfully"
            if property.archived
            else "Property unarchived successfully"
        )
        return {"message": message}, 200


class ArchiveProperties(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("ids", action="append")

    @admin_required
    def patch(self):
        data = ArchiveProperties.parser.parse_args()
        propertyList = []

        if not ("ids" in data and type(data["ids"]) is list):
            return {"message": "Property IDs missing in request"}, 400

        for id in data["ids"]:
            property = PropertyModel.find(id)
            property.archived = True
            propertyList.append(property)

        db.session.bulk_save_objects(propertyList)
        db.session.commit()
        return {"properties": [p.json() for p in PropertyModel.query.all()]}, 200


# single property/name
class Property(Resource):
    @admin_required
    def get(self, id):
        property = PropertyModel.find(id)
        property_json = property.json()
        property_json["tenants"] = property.tenants()
        return property_json

    @admin_required
    def delete(self, id):
        property = PropertyModel.find(id)
        property.delete_from_db()
        return {"message": "Property deleted"}

    @admin_required
    def put(self, id):
        property = PropertyModel.find(id)
        payload = request.json
        context = {"name": property.name}

        return PropertyModel.update(
            schema=PropertySchema, id=id, context=context, payload=payload
        ).json()
