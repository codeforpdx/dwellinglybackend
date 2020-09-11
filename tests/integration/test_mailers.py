import pytest
from conftest import is_valid
from unittest.mock import patch
from flask_mail import Mail


@pytest.mark.usefixtures('client_class', 'test_database')
class TestPostEmail:
    def setup(self):
        self.endpoint = '/api/user/message'

    @patch.object(Mail, 'send')
    def test_email_can_be_sent(self, send_mail_msg, auth_headers):
        payload = {
                'userid': 1,
                'title': 'Some email subject',
                'body': 'Some body'
            }
        
        response = self.client.post(
                self.endpoint,
                json=payload,
                headers=auth_headers["admin"]
            )
        assert is_valid(response, 200)
        send_mail_msg.assert_called()
        assert response.json == {"Message": "Message Sent"}

    @patch.object(Mail, 'send')
    def test_user_id_param_is_required(self, send_mail_msg, auth_headers):
        payload = {
                'title': 'Some email subject',
                'body': 'Some body'
            }
        response = self.client.post(
                self.endpoint,
                json=payload,
                headers=auth_headers["admin"]
            )

        assert response.status == '400 BAD REQUEST'
        send_mail_msg.assert_not_called()

    @patch.object(Mail, 'send')
    def test_subject_param_is_required(self, send_mail_msg, auth_headers):
        payload = {
                'userid': 1,
                'body': 'Some body'
            }
        response = self.client.post(
                self.endpoint,
                json=payload,
                headers=auth_headers["admin"]
            )

        assert response.status == '400 BAD REQUEST'
        send_mail_msg.assert_not_called()

    @patch.object(Mail, 'send')
    def test_body_param_is_required(self, send_mail_msg, auth_headers):
        payload = {
                'userid': 1,
                'title': 'Some email subject',
            }
        response = self.client.post(
                self.endpoint,
                json=payload,
                headers=auth_headers["admin"]
            )

        assert response.status == '400 BAD REQUEST'
        send_mail_msg.assert_not_called()


@pytest.mark.usefixtures('client_class', 'test_database')
class TestEmailAuthorizations:
    def setup(self):
        self.endpoint = '/api/user/message'

    def test_auth_header_is_required(self):
        response = self.client.post(self.endpoint)
    
        assert is_valid(response, 401)
        assert response.json == {'msg': 'Missing Authorization Header'}

    def test_all_roles_except_admin_are_denied_access(self, auth_headers):
        payload = {
                'userid': 1,
                'title': 'Some email subject',
                'body': 'Some body'
            }
        for role, token in auth_headers.items():
            if role != 'admin':
                response = self.client.post(self.endpoint, json=payload, headers=token)
                assert is_valid(response, 401)
                assert response.json == {'message': "Admin Access Required"}
