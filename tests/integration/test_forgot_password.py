import pytest
from models.user import UserModel
from conftest import is_valid

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
         
