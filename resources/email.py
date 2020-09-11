from flask import Flask, current_app
from flask_restful import Resource, reqparse
from flask_mail import Message
from resources.admin_required import admin_required
from models.user import UserModel

class Email(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('userid', required=True)
    parser.add_argument('title', required=True)
    parser.add_argument('body', required=True)

    @admin_required
    def post(self):
        data = Email.parser.parse_args()

        message = Message(data.title, sender="noreply@codeforpdx.org", body=data.body )

        user = UserModel.find_by_id(data.userid)
        message.recipients = [user.email]

        current_app.mail.send(message)
        return {"Message": "Message Sent"}


    @staticmethod
    def send_reset_password_msg(user):
        pass
