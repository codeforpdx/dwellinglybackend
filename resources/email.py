from flask import Flask, current_app, render_template
from flask_restful import Resource, reqparse
from flask_mail import Message
from resources.admin_required import admin_required
from models.user import UserModel

class Email(Resource):
    NO_REPLY = 'noreply@codeforpdx.org'
    parser = reqparse.RequestParser()
    parser.add_argument('user_id', required=True)
    parser.add_argument('subject', required=True)
    parser.add_argument('body', required=True)

    @admin_required
    def post(self):
        data = Email.parser.parse_args()
        user = UserModel.find_by_id(data.user_id)

        message = Message(data.subject, sender=Email.NO_REPLY, body=data.body )
        message.recipients = [user.email]

        current_app.mail.send(message)
        return {"Message": "Message Sent"}


    @staticmethod
    def send_reset_password_msg(user):
        token = user.reset_password_token()
        msg = Message('Reset password', sender=Email.NO_REPLY, recipients=[user.email])
        msg.body = render_template('emails/reset_msg.txt', user=user, token=token)
        msg.html = render_template('emails/reset_msg.html', user=user, token=token)

        current_app.mail.send(msg)
