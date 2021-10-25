from app import create_app
import os
from flask import render_template


class TestEmailTemplateRender:

    FRONTEND_BASE_URL = "http://localhost:3000"

    def test_reset_password_html_msg(self, user_attributes):
        user = user_attributes()

        token = "fake-token"
        app = create_app(os.getenv("FLASK_ENV"))
        templates = [
            "emails/reset_msg.html",
            "emails/reset_msg.txt",
            "emails/invite_user_msg.html",
            "emails/invite_user_msg.txt",
        ]

        with app.app_context():
            for template in templates:
                email = render_template(
                    template,
                    FRONTEND_BASE_URL=self.FRONTEND_BASE_URL,
                    user=user,
                    token=token,
                )

                link = "http://localhost:3000/changePassword?token={}".format(token)
                assert link in email

    def test_hyperlink_is_https(self):
        app = create_app(os.getenv("FLASK_ENV"))

        with app.app_context():
            FRONTEND_BASE_URL = app.config["FRONTEND_BASE_URL"]
            assert FRONTEND_BASE_URL.startswith("http://")
