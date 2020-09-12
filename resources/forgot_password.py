from flask_restful import Resource, reqparse
from models.user import UserModel
from resources.email import Email


class ForgotPassword(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('email', required=True)

    def post(self):
        data = ForgotPassword.parser.parse_args()
        user = UserModel.find_by_email(data['email'])

        if user:
            Email.send_reset_password_msg(user)
            return {"message": "Email sent"}, 200
        else:
            return {"message": "Invalid email"}, 400

    def get(self, token):
        user = UserModel.validate_reset_password(token)

        if user:
            return {'message': 'Valid token', 'user_id': user.id}, 200
        else:
            return {'message': 'Expired token'}, 422
