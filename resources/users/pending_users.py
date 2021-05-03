from flask_restful import Resource
from models.user import UserModel
from utils.authorizations import admin_required


class UsersPending(Resource):
    @admin_required
    def get(self):
        return {"users": UserModel.find_users_without_assigned_role().json()}
