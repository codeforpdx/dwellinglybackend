from flask_restful import Resource
from flask import request
from utils.authorizations import admin_required
from models.users.property_manager import PropertyManager
from models.users.staff import Staff
from models.users.admin import Admin
from schemas import UserSchema
from resources.email import Email
from models.user import RoleEnum
import string
import random


class UserInvite(Resource):
    @admin_required
    def post(self):
        temp_password = "".join(random.choice(string.ascii_lowercase) for i in range(8))

        user_class = self.user_type(request.json.get("type", request.json.get("role")))
        user = user_class.create(
            schema=UserSchema, payload={**request.json, "password": temp_password}
        )
        Email.send_user_invite_msg(user)
        return {"message": "User Invited"}, 201

    def user_type(self, value):
        if value == RoleEnum.PROPERTY_MANAGER.value or value == "property_manager":
            return PropertyManager
        elif value == RoleEnum.STAFF.value or value == "staff":
            return Staff
        elif value == RoleEnum.ADMIN.value or value == "admin":
            return Admin
