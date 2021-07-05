from flask import render_template
from flask_mailman import EmailMultiAlternatives


class Email:
    # TODO: Update this
    NO_REPLY = "noreply@codeforpdx.org"

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
