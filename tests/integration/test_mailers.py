import pytest
from conftest import is_valid
from unittest.mock import patch
from flask_mailman import EmailMessage
from resources.email import Email


@pytest.mark.usefixtures("client_class", "empty_test_db")
class TestPostEmail:
    def setup(self):
        self.endpoint = "/api/user/message"

    @patch.object(EmailMessage, "send")
    def test_email_can_be_sent(self, send_mail_msg, create_admin_user, valid_header):
        payload = {
            "user_id": create_admin_user().id,
            "subject": "Some email subject",
            "body": "Some body",
        }

        with patch.object(EmailMessage, "__init__", return_value=None):
            response = self.client.post(
                self.endpoint, json=payload, headers=valid_header
            )
        assert is_valid(response, 200)
        send_mail_msg.assert_called()
        assert response.json == {"message": "Message sent"}

    @patch.object(EmailMessage, "send")
    def test_user_id_param_is_required(self, send_mail_msg, valid_header):
        payload = {"subject": "Some email subject", "body": "Some body"}
        response = self.client.post(self.endpoint, json=payload, headers=valid_header)

        assert response.status == "400 BAD REQUEST"
        send_mail_msg.assert_not_called()

    @patch.object(EmailMessage, "send")
    def test_subject_param_is_required(self, send_mail_msg, valid_header):
        payload = {"user_id": 1, "body": "Some body"}
        response = self.client.post(self.endpoint, json=payload, headers=valid_header)

        assert response.status == "400 BAD REQUEST"
        send_mail_msg.assert_not_called()

    @patch.object(EmailMessage, "send")
    def test_body_param_is_required(self, send_mail_msg, valid_header):
        payload = {
            "user_id": 1,
            "subject": "Some email subject",
        }
        response = self.client.post(self.endpoint, json=payload, headers=valid_header)

        assert response.status == "400 BAD REQUEST"
        send_mail_msg.assert_not_called()


@pytest.mark.usefixtures("empty_test_db")
class TesttEmail:
    @patch.object(EmailMessage, "send")
    def test_reset_password_msg(self, send_mail_msg, new_user):
        with patch.object(EmailMessage, "__init__", return_value=None):
            Email.send_reset_password_msg(new_user)

        send_mail_msg.assert_called()

    @patch.object(EmailMessage, "send")
    def test_send_user_invite_msg(self, send_mail_msg, new_user):
        with patch.object(EmailMessage, "__init__", return_value=None):
            Email.send_user_invite_msg(new_user)
        send_mail_msg.assert_called()
