from flask_restful import Resource, reqparse
from flask import request
from utils.authorizations import admin_required
from db import db
from models.property import PropertyModel
from schemas.property import PropertySchema


class Properties(Resource):
    def get(self):
        return {"properties": PropertyModel.query.json()}

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


class Property(Resource):
    @admin_required
    def get(self, id):
        return PropertyModel.find(id).json(include_tenants=True)

    @admin_required
    def delete(self, id):
        PropertyModel.delete(id)
        return {"message": "Property deleted"}

    @admin_required
    def put(self, id):
        property = PropertyModel.find(id)

        return PropertyModel.update(
            schema=PropertySchema,
            id=id,
            context={"name": property.name},
            payload=request.json,
        ).json()
