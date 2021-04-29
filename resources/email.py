from flask import render_template
from flask_restful import Resource, reqparse
from flask_mailman import EmailMessage, EmailMultiAlternatives
from utils.authorizations import admin_required
from models.user import UserModel


class Email(Resource):
    NO_REPLY = "noreply@codeforpdx.org"  # Should this be dwellingly address?

    parser = reqparse.RequestParser()
    parser.add_argument("user_id", required=True)
    parser.add_argument("subject", required=True)
    parser.add_argument("body", required=True)

    @admin_required
    def post(self):
        data = Email.parser.parse_args()
        user = UserModel.find(data.user_id)

        msg = EmailMessage(data.subject, data.body, Email.NO_REPLY, [user.email])
        msg.send()
        return {"message": "Message sent"}

    @staticmethod
    def send_reset_password_msg(user):
        token = user.reset_password_token()
        msg = EmailMultiAlternatives(
            "Rest password for Dwellingly",
            render_template("emails/reset_msg.html", user=user, token=token),
            Email.NO_REPLY,
            [user.email],
        )
        msg.content_subtype = "html"

        msg.attach_alternative(
            render_template("emails/reset_msg.txt", user=user, token=token),
            "text/plain",
        )

        msg.send()

    @staticmethod
    def send_user_invite_msg(user):
        token = user.reset_password_token()
        msg = EmailMultiAlternatives(
            "Create Your Dwellingly Account",
            render_template("emails/invite_user_msg.html", user=user, token=token),
            Email.NO_REPLY,
            [user.email],
        )
        msg.content_subtype = "html"
        msg.attach_alternative(
            render_template("emails/invite_user_msg.txt", user=user, token=token),
            "text/plain",
        )
        msg.send()
