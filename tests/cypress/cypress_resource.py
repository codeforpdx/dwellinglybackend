from flask import current_app, request, abort
from flask_restful import Resource

from db import db
from models.user import RoleEnum
from models.staff_tenant_link import StaffTenantLink
from models.user import UserModel
from models.users.staff import Staff
from models.tenant import TenantModel
from schemas.user import UserSchema, UserRegisterSchema
from schemas.tenant import TenantSchema


def protected_env(func):
    def _decorator(*args, **kwargs):
        if current_app.env == "testing":
            return func(*args, **kwargs)
        abort(404)

    return _decorator


not_found_message = {"message": "RequestNotFoundError: Request was not found"}


class CypressResource(Resource):
    @protected_env
    def post(self):
        if request.args.get("setup"):
            self._setup()
            return 200

        if request.args.get("create_pending_user"):
            UserModel.create(
                schema=UserRegisterSchema,
                payload=request.json,
            )
            return 200

        if request.args.get("create_staff_user"):
            Staff.create(
                schema=UserSchema,
                payload={**request.json, "role": RoleEnum.STAFF.value},
            )
            return 200

        if request.args.get("create_tenant"):
            TenantModel.create(schema=TenantSchema, payload=(request.json))
            return 200

        return not_found_message, 421

    def _setup(self):
        for st in StaffTenantLink.query.all():
            self._del(st)
        for u in UserModel.query.where(UserModel.email != "user1@dwellingly.org").all():
            self._del(u)
        for t in TenantModel.query.all():
            self._del(t)

        self._commit()

    def _del(self, obj):
        db.session.delete(obj)

    def _commit(self):
        db.session.commit()
