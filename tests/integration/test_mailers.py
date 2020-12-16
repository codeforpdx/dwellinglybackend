import pytest
from conftest import is_valid
from unittest.mock import patch
from flask_mail import Mail, Message
from resources.email import Email


@pytest.mark.usefixtures('client_class', 'empty_test_db')
class TestPostEmail:
    def setup(self):
        self.endpoint = '/api/user/message'

    @patch.object(Mail, 'send')
    def test_email_can_be_sent(self, send_mail_msg, create_admin_user, valid_header):
        payload = {
                'user_id': create_admin_user().id,
                'subject': 'Some email subject',
                'body': 'Some body'
            }

        with patch.object(Message, '__init__', return_value=None):
            response = self.client.post(
                self.endpoint,
                json=payload,
                headers=valid_header
            )
        assert is_valid(response, 200)
        send_mail_msg.assert_called()
        assert response.json == {"message": "Message sent"}

    @patch.object(Mail, 'send')
    def test_user_id_param_is_required(self, send_mail_msg, valid_header):
        payload = {
                'subject': 'Some email subject',
                'body': 'Some body'
            }
        response = self.client.post(
                self.endpoint,
                json=payload,
                headers=valid_header
            )

        assert response.status == '400 BAD REQUEST'
        send_mail_msg.assert_not_called()

    @patch.object(Mail, 'send')
    def test_subject_param_is_required(self, send_mail_msg, valid_header):
        payload = {
                'user_id': 1,
                'body': 'Some body'
            }
        response = self.client.post(
                self.endpoint,
                json=payload,
                headers=valid_header
            )

        assert response.status == '400 BAD REQUEST'
        send_mail_msg.assert_not_called()

    @patch.object(Mail, 'send')
    def test_body_param_is_required(self, send_mail_msg, valid_header):
        payload = {
                'user_id': 1,
                'subject': 'Some email subject',
            }
        response = self.client.post(
                self.endpoint,
                json=payload,
                headers=valid_header
            )

        assert response.status == '400 BAD REQUEST'
        send_mail_msg.assert_not_called()


@pytest.mark.usefixtures('client_class', 'empty_test_db')
class TestEmailAuthorizations:
    def setup(self):
        self.endpoint = '/api/user/message'

    def test_auth_header_is_required(self):
        response = self.client.post(self.endpoint)

        assert is_valid(response, 401)
        assert response.json == {'message': 'Missing authorization header'}

    def test_all_roles_except_admin_are_denied_access(self, auth_headers):
        payload = {
                'user_id': 1,
                'subject': 'Some email subject',
                'body': 'Some body'
            }
        for role, token in auth_headers.items():
            if role != 'admin':
                response = self.client.post(self.endpoint, json=payload, headers=token)
                assert is_valid(response, 401)
                assert response.json == {'message': "Admin access required"}


@pytest.mark.usefixtures('empty_test_db')
class TesttEmail:
    @patch.object(Mail, 'send')
    def test_reset_password_msg(self, send_mail_msg, new_user):
        with patch.object(Message, '__init__', return_value=None):
            Email.send_reset_password_msg(new_user)

        send_mail_msg.assert_called()

    @patch.object(Mail, 'send')
    def test_send_user_invite_msg(self, send_mail_msg, new_user):
        with patch.object(Message, '__init__', return_value=None):
            Email.send_user_invite_msg(new_user)
        send_mail_msg.assert_called()
