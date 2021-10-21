from app import create_app
import os
from flask import render_template


class TestEmailTemplateRender:
    def test_reset_password_html_msg(self, user_attributes):
        user = user_attributes()
        # need to find a user fixture and a token fixture
        token = "fake-token"
        app = create_app(os.getenv("FLASK_ENV"))
        templates = [
            "emails/reset_msg.html",
            "emails/reset_msg.txt",
            "emails/invite_user_msg.html",
            "emails/invite_user_msg.txt",
        ]

        with app.app_context():
            FRONTEND_BASE_URL = app.config["FRONTEND_BASE_URL"]

            for template in templates:

                email = render_template(
                    template,
                    FRONTEND_BASE_URL=FRONTEND_BASE_URL,
                    user=user,
                    token=token,
                )

                link = "{}/changePassword?token={}".format(FRONTEND_BASE_URL, token)

                assert link in email

    def test_hyperlink_is_https(self):
        app = create_app(os.getenv("FLASK_ENV"))

        with app.app_context():
            FRONTEND_BASE_URL = app.config["FRONTEND_BASE_URL"]
            assert FRONTEND_BASE_URL.startswith("https://")
