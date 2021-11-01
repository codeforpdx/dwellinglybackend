from flask_restful import Resource

from utils.authorizations import admin_required
from models.user import UserModel


class UsersPending(Resource):
    @admin_required
    def get(self):
        return {"users": UserModel.query.active().pending().json()}
