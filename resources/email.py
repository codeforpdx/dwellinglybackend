from flask import render_template
from flask import current_app as app
from flask_mailman import EmailMultiAlternatives


class Email:
    # TODO: Update this
    NO_REPLY = "noreply@codeforpdx.org"

    @staticmethod
    def send_reset_password_msg(user):
        token = user.reset_password_token()
        FRONTEND_BASE_URL = app.config["FRONTEND_BASE_URL"]
        msg = EmailMultiAlternatives(
            "Reset password for Dwellingly",
            render_template(
                "emails/reset_msg.html",
                FRONTEND_BASE_URL=FRONTEND_BASE_URL,
                user=user,
                token=token,
            ),
            Email.NO_REPLY,
            [user.email],
        )
        msg.content_subtype = "html"

        msg.attach_alternative(
            render_template(
                "emails/reset_msg.txt",
                FRONTEND_BASE_URL=FRONTEND_BASE_URL,
                user=user,
                token=token,
            ),
            "text/plain",
        )

        msg.send()

    @staticmethod
    def send_user_invite_msg(user):
        token = user.reset_password_token()
        FRONTEND_BASE_URL = app.config["FRONTEND_BASE_URL"]
        msg = EmailMultiAlternatives(
            "Create Your Dwellingly Account",
            render_template(
                "emails/invite_user_msg.html",
                FRONTEND_BASE_URL=FRONTEND_BASE_URL,
                user=user,
                token=token,
            ),
            Email.NO_REPLY,
            [user.email],
        )
        msg.content_subtype = "html"
        msg.attach_alternative(
            render_template(
                "emails/invite_user_msg.txt",
                FRONTEND_BASE_URL=FRONTEND_BASE_URL,
                user=user,
                token=token,
            ),
            "text/plain",
        )
        msg.send()
