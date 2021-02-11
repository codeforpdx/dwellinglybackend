from flask_restful import Resource
from models.user import UserModel
from utils.authorizations import admin_required


class UsersPending(Resource):
    @admin_required
    def get(self):
        users = [user.json() for user in UserModel.find_unassigned_users()]
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
