import pytest
from unittest.mock import patch
from flask_mailman import EmailMessage
from resources.email import Email


@pytest.mark.usefixtures("empty_test_db")
class TesttEmail:
    @patch.object(EmailMessage, "send")
    def test_reset_password_msg(self, send_mail_msg, create_user):
        with patch.object(EmailMessage, "__init__", return_value=None):
            Email.send_reset_password_msg(create_user())

        send_mail_msg.assert_called()

    @patch.object(EmailMessage, "send")
    def test_send_user_invite_msg(self, send_mail_msg, create_user):
        with patch.object(EmailMessage, "__init__", return_value=None):
            Email.send_user_invite_msg(create_user())
        send_mail_msg.assert_called()
