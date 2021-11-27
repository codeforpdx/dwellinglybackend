from flask import current_app, request, abort
from flask_restful import Resource

from data.seed import Seed
from models.user import RoleEnum
from models.users.staff import Staff
from models.tenant import TenantModel
from schemas.user import UserSchema
from schemas.tenant import TenantSchema


def protected_env(func):
    def _decorator(*args, **kwargs):
        if current_app.env == "testing":
            return func(*args, **kwargs)
        abort(404)

    return _decorator


seed = Seed()
not_found_message = {"message": "RequestNotFoundError: Request was not found"}


class CypressResource(Resource):
    @protected_env
    def post(self):
        if request.args.get("setup"):
            self._setup()
            return 200

        if request.args.get("create_pending_user"):
            seed.create_pending_user(payload=request.json)
            return 200

        if request.args.get("create_staff_user"):
            Staff.create(
                schema=UserSchema,
                payload={**request.json, "role": RoleEnum.STAFF.value},
            )
            return 200

        if request.args.get("create_property_manager"):
            seed.create_property_manager(request.json)
            return 200

        if request.args.get("create_tenant"):
            TenantModel.create(schema=TenantSchema, payload=(request.json))
            return 200

        return not_found_message, 421

    def _setup(self):
        seed.destroy_all()
        seed.create_admin()
