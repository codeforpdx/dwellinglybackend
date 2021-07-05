from flask import request
from flask_restful import Resource
from models.user import UserModel
from resources.email import Email


class ResetPassword(Resource):
    def post(self):
        user = UserModel.find_by_email(request.json.get("email", ""))

        if user:
            Email.send_reset_password_msg(user)
            return {"message": "Email sent"}, 200
        else:
            return {"message": "Invalid email"}, 400

    def get(self, token):
        user = UserModel.validate_reset_password(token)

        if user:
            return {"message": "Valid token", "user_id": user.id}, 200
        else:
            return {"message": "Expired token"}, 422
