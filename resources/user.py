from flask_restful import Resource, reqparse
from flask import request
from schemas import UserRegisterSchema, UserSchema
from utils.authorizations import admin_required, pm_level_required
from models.user import UserModel, RoleEnum
from models.revoked_tokens import RevokedTokensModel
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt,
    get_jwt_identity,
    jwt_required,
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
        current_user = UserModel.find(get_jwt_identity())
        user = UserModel.find(id)
        role = request.json.get("role")
        password = request.json.get("new_password")

        if not self._authorized(current_user=current_user, user=user, role_change=role):
            return {"message": "Not Authorized"}, 403

        if role:
            user.role = RoleEnum(role)
            user.type = RoleEnum(role).name.lower()

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

        if user.id == get_jwt_identity():
            return {"message": "Cannot delete self"}, 400

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
        if RoleEnum.has_role(int(request.args["r"])):
            return {
                "users": UserModel.query.filter_by(
                    role=RoleEnum(int(request.args["r"]))
                ).json()
            }
        else:
            return {"message": "Invalid role"}, 400
