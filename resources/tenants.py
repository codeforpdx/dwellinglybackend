from flask_restful import Resource
from flask import request
from utils.authorizations import admin_required
from models.tenant import TenantModel
from schemas.tenant import TenantSchema


class Tenant(Resource):
    @admin_required
    def get(self, id):
        return TenantModel.find(id).json()

    @admin_required
    def put(self, id):
        tenant = TenantModel.find(id)
        return tenant.update(schema=TenantSchema, payload=request.json).json()


class Tenants(Resource):
    @admin_required
    def get(self):
        if request.args.get("unstaffed"):
            return {
                "tenants": TenantModel.query.active()
                .unassigned_staff()
                .order_by(TenantModel.updated_at.asc())
                .json()
            }

        return {"tenants": TenantModel.query.json()}

    @admin_required
    def post(self):
        return (
            TenantModel.create(schema=TenantSchema, payload=request.json).json(),
            201,
        )
