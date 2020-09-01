import pytest
from models.user import UserModel
from conftest import is_valid
from unittest.mock import patch
from resources.email import Email


@pytest.mark.usefixtures('client_class', 'test_database')
class TestForgotPassword:
    def test_request_with_invalid_params(self):
        response = self.client.post('/api/forgot_password')
        assert is_valid(response, 400)
        assert response.json == {'message': {'email': 'This field cannot be blank.'}}

    def test_response_with_invalid_email(self):
        response = self.client.post('/api/forgot_password', json={'email': 'invalid@example.org'})
        assert is_valid(response, 400)
        assert response.json == {'message': 'Unable to find email'}

    def test_response_with_valid_email(self):
        user = UserModel.find_by_id(1)
        response = self.client.post('/api/forgot_password', json={'email': user.email})

        assert is_valid(response, 200)
        assert response.json == user.json()

    @patch.object(Email, 'send_reset_password_msg')
    def test_password_reset_email_sent(self, stubbed_reset_password_method):
        user = UserModel.find_by_id(1)

        response = self.client.post('/api/forgot_password', json={'email': user.email})

        stubbed_reset_password_method.assert_called_once_with(user)
        assert is_valid(response, 200)
