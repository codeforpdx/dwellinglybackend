from flask_restful import Resource, reqparse
from models.user import UserModel


class ForgotPassword(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('email',type=str,required=True,help="This field cannot be blank.")

    def post(self):
        data = ForgotPassword.parser.parse_args()
        user = UserModel.find_by_email(data['email'])

        if user:
            return user.json(), 200
        else:
            return {"message": "Unable to find email"}, 400