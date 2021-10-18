from flask_restful import Resource
from flask import request
from utils.authorizations import admin_required
from db import db
from models.property import PropertyModel
from schemas.property import PropertySchema


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

        return property.update(schema=PropertySchema, payload=request.json).json()


class Properties(Resource):
    @admin_required
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
    @admin_required
    def patch(self):
        if not ("ids" in request.json and type(request.json["ids"]) is list):
            return {"message": "Property IDs missing in request"}, 400

        properties = []
        for id in request.json["ids"]:
            property = PropertyModel.find(id)
            property.archived = True
            properties.append(property)

        db.session.bulk_save_objects(properties)
        db.session.commit()
        return {"properties": PropertyModel.query.json()}
