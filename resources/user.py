from flask_restful import Resource
from flask import request
from schemas import UserRegisterSchema, UserSchema
from utils.authorizations import admin_required, pm_level_required
from models.user import UserModel, RoleEnum, UserTypes
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    current_user,
)


class UserRegister(Resource):
    def post(self):
        UserModel.create(schema=UserRegisterSchema, payload=request.json)

        return {"message": "User created successfully."}, 201


class User(Resource):
    @admin_required
    def get(self, id):
        return UserModel.find(id).json()

    @pm_level_required
    def patch(self, id):
        user = UserModel.find(id)
        role = request.json.get("role")
        user_type = UserTypes.get(request.json.get("type"))
        password = request.json.get("new_password")
        role_change = role or user_type

        if not self._authorized(
            current_user=current_user, user=user, role_change=role_change
        ):
            return {"message": "Not Authorized"}, 403

        if role:
            user.role = RoleEnum(role)
            user.type = RoleEnum(role).name.lower()

        if user_type:
            user.type = user_type

        if password:
            if password != request.json.get("confirm_password"):
                return {"message": "Unconfirmed password"}, 422
            if user.check_pw(request.json.get("current_password")):
                user.password = password
            else:
                return {"message": "Password does not match."}, 401

        return user.update(schema=UserSchema, payload=request.json).json(
            refresh_token=current_user == user
        )

    def _authorized(self, current_user, user, role_change):
        if role_change or current_user != user:
            return current_user.is_admin()
        else:
            return True

    @admin_required
    def delete(self, id):
        user = UserModel.find(id)

        if user == current_user:
            return {"message": "Cannot delete self"}, 400

        user.delete_from_db()
        return {"message": "User deleted"}


class ArchiveUser(Resource):
    @admin_required
    def post(self, user_id):
        if user_id == current_user.id:
            return {"message": "Cannot archive self"}, 400

        user = UserModel.find(user_id)

        user.archived = not user.archived

        user.save_to_db()

        return user.json(), 201


class UserLogin(Resource):
    def post(self):
        return UserModel.authenticate(
            UserModel.find_by_email(request.json.get("email", "")),
            request.json.get("password", ""),
        )


# This endpoint allows the app to use a refresh token to get a new access token
class UserAccessRefresh(Resource):

    # The jwt_required(refresh=True) decorator insures a valid refresh
    # token is present in the request before calling this endpoint. We
    # can use the get_jwt_identity() function to get the identity of
    # the refresh token, and use the create_access_token() function again
    # to make a new access token for this identity.
    @jwt_required(refresh=True)
    def post(self):
        ret = {"access_token": create_access_token(identity=current_user)}
        return ret, 200


class Users(Resource):
    @admin_required
    def get(self):
        user_type = UserTypes.get(request.args.get("type"))
        # TODO: This is temporary. Switching to type from role lookup.
        if RoleEnum.has_role(int(request.args.get("r", 99))):
            return {
                "users": UserModel.query.filter_by(
                    role=RoleEnum(int(request.args["r"]))
                ).json()
            }
        elif user_type:
            return {"users": UserModel.query.filter_by(type=user_type).json()}

        return {"message": "Invalid role"}, 400
