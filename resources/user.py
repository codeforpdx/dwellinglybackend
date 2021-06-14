from flask_restful import Resource, reqparse
from flask import request
from schemas import UserRegisterSchema
from models.property import PropertyModel
from utils.authorizations import admin_required, admin, pm_level_required
from models.user import UserModel, RoleEnum
from models.revoked_tokens import RevokedTokensModel
import json
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt,
    get_jwt_identity,
    jwt_required,
)


class UserRoles(Resource):
    def get(self):
        roles = {}
        for role in RoleEnum:
            roles[role.name] = role.value
        result = json.dumps(roles)
        return result, 200


class UserRegister(Resource):
    def post(self):
        UserModel.create(schema=UserRegisterSchema, payload=request.json)

        return {"message": "User created successfully."}, 201


class User(Resource):
    @admin_required
    def get(self, user_id):
        return UserModel.find(user_id).json()

    @pm_level_required
    def patch(self, user_id):

        user = UserModel.find(user_id)

        parser = reqparse.RequestParser()
        parser.add_argument(
            "role", type=int, required=False, help="This field is not required"
        )
        parser.add_argument(
            "firstName", type=str, required=False, help="This field is not required"
        )
        parser.add_argument(
            "lastName", type=str, required=False, help="This field is not required"
        )
        parser.add_argument(
            "email", type=str, required=False, help="This field is not required"
        )
        parser.add_argument(
            "phone", type=str, required=False, help="This field is not required"
        )
        parser.add_argument(
            "current_password",
            type=str,
            required=False,
            help="This field is not required",
        )
        parser.add_argument(
            "new_password", type=str, required=False, help="This field is not required"
        )
        parser.add_argument(
            "confirm_password",
            type=str,
            required=False,
            help="This field is not required",
        )

        data = parser.parse_args()

        if user_id != get_jwt_identity() and not admin():
            return (
                {
                    "message": "You cannot change another user's information \
                    unless you are an admin"
                },
                403,
            )

        if data["role"] and not admin():
            return {"message": "Only admins can change roles"}, 403

        if data["role"]:
            user.role = RoleEnum(data["role"])
            user.type = RoleEnum(data["role"]).name.lower()
        if data["firstName"] is not None:
            user.firstName = data["firstName"]
        if data["lastName"] is not None:
            user.lastName = data["lastName"]
        if data["email"]:
            user.email = data["email"]
        if data["phone"]:
            user.phone = data["phone"]

        # Reset Password
        if (
            data["current_password"]
            and data["new_password"]
            and data["confirm_password"]
        ):

            # Step #1: Check if current password matches the one in the db
            if not user.check_pw(data["current_password"]):
                return {"message": "Password does not match."}, 401

            # Step #2: Check if new password and confirm password match
            if data["new_password"] != data["confirm_password"]:
                return {"message": "New password does not match."}, 422

            # Step #3: Set the new password
            user.password = data["new_password"]

        user.save_to_db()

        if user_id == get_jwt_identity():
            new_tokens = {
                "access_token": create_access_token(identity=user.id, fresh=True),
                "refresh_token": create_refresh_token(user.id),
            }
            user.update_last_active()
            return {**user.json(), **new_tokens}, 201

        return user.json(), 201

    @admin_required
    def delete(self, user_id):
        if user_id == get_jwt_identity():
            return {"message": "Cannot delete self"}, 400

        user = UserModel.find(user_id)

        user.delete_from_db()
        return {"message": "User deleted"}, 200


class ArchiveUser(Resource):
    @admin_required
    def post(self, user_id):
        if user_id == get_jwt_identity():
            return {"message": "Cannot archive self"}, 400

        user = UserModel.find(user_id)

        user.archived = not user.archived

        user.save_to_db()

        if user.archived:
            # invalidate access token
            jti = get_jwt()["jti"]
            revokedToken = RevokedTokensModel(jti=jti)
            revokedToken.save_to_db()

        return user.json(), 201


class UserLogin(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "email", type=str, required=True, help="This field cannot be blank"
    )
    parser.add_argument(
        "password", type=str, required=True, help="This field cannot be blank"
    )

    def post(self):
        data = UserLogin.parser.parse_args()

        user = UserModel.find_by_email(data["email"])

        if user and (user.archived or user.role is None):
            return {"message": "Invalid user"}, 403

        if user and user.check_pw(data["password"]):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            user.update_last_active()
            return {"access_token": access_token, "refresh_token": refresh_token}, 200

        return {"message": "Invalid credentials"}, 401


class UsersRole(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "userrole", type=int, required=True, help="This field cannot be blank"
    )
    parser.add_argument("name", type=str, required=False)

    @admin_required
    def post(self):
        data = UsersRole.parser.parse_args()
        if data["name"]:
            users = UserModel.find_by_role_and_name(
                RoleEnum(data["userrole"]), data["name"]
            )
        else:
            users = UserModel.find_by_role(RoleEnum(data["userrole"]))
        users_info = []
        for user in users:
            info = user.json()
            info["properties"] = [
                p.json() for p in PropertyModel.find_by_manager(user.id) if p
            ]
            users_info.append(info)
        return {"users": users_info}


# This endpoint allows the app to use a refresh token to get a new access token
class UserAccessRefresh(Resource):

    # The jwt_required(refresh=True) decorator insures a valid refresh
    # token is present in the request before calling this endpoint. We
    # can use the get_jwt_identity() function to get the identity of
    # the refresh token, and use the create_access_token() function again
    # to make a new access token for this identity.
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        ret = {"access_token": create_access_token(identity=current_user)}
        return ret, 200


class Users(Resource):
    @admin_required
    def get(self):

        role_query = int(request.args["r"])

        if not RoleEnum.has_role(role_query):
            return {"message": "Invalid role"}, 400

        role = RoleEnum(role_query)
        users = [user.json() for user in UserModel.find_by_role(role)]
        ret = [
            {
                "id": user["id"],
                "firstName": user["firstName"],
                "lastName": user["lastName"],
                "email": user["email"],
                "phone": user["phone"],
                "role": user["role"],
                "tickets": "TODO",
                "tenants": "TODO",
            }
            for user in users
        ]

        return {"users": ret}, 200
