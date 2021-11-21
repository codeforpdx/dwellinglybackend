import string
import random
from flask_restful import Resource
from flask import request

from utils.authorizations import admin_required
from models.user import UserModel
from models.users.property_manager import PropertyManager
from schemas import UserSchema, PropertyManagerSchema
from resources.email import Email


class UserInvite(Resource):
    @admin_required
    def post(self):
        data = request.json
        temp_password = "".join(random.choice(string.ascii_lowercase) for i in range(8))
        user = UserModel.create(
            schema=UserSchema, payload={**data, "password": temp_password}
        )
        Email.send_user_invite_msg(user)
        return {"message": "User Invited"}, 201


class PropertyManagerInviteResource(Resource):
    @admin_required
    def post(self):
        property_manager = PropertyManager.create(
            schema=PropertyManagerSchema, payload=request.json
        )
        Email.send_user_invite_msg(property_manager)
        return {"message": "Property Manager Invited"}, 201
