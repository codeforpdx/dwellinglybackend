import pytest
from conftest import is_valid
from unittest.mock import patch
from resources.email import Email
from freezegun import freeze_time
from utils.time import Time


@pytest.mark.usefixtures("client_class")
class TestResetPasswordPOST:
    def setup(self):
        self.endpoint = "/api/reset-password"

    def test_request_with_invalid_params(self):
        response = self.client.post(self.endpoint, json={})
        assert is_valid(response, 400)

    def test_request_with_invalid_email(self):
        response = self.client.post(
            self.endpoint, json={"email": "invalid@example.org"}
        )
        assert is_valid(response, 400)
        assert response.json == {"message": "Invalid email"}

    @patch.object(Email, "send_reset_password_msg")
    def test_request_with_valid_email(self, send_reset_email, create_user):
        user = create_user()
        response = self.client.post(self.endpoint, json={"email": user.email})

        assert is_valid(response, 200)
        assert response.json == {"message": "Email sent"}
        send_reset_email.assert_called_once_with(user)

    @patch.object(Email, "send_reset_password_msg")
    def test_request_with_invalid_user(self, send_reset_email):
        response = self.client.post(
            self.endpoint, json={"email": "invalid_email@nickschimek.com"}
        )

        send_reset_email.assert_not_called()
        assert is_valid(response, 400)


@pytest.mark.usefixtures("client_class")
class TestResetPasswordGET:
    def setup(self):
        self.endpoint = "/api/reset-password"

    def test_request_with_invalid_params(self):
        response = self.client.get(f"{self.endpoint}/garbage_request")
        assert response.status == "422 UNPROCESSABLE ENTITY"
        assert response.json == {"message": "Not enough segments"}

    def test_request_with_expired_token(self, create_user):
        with freeze_time(Time.yesterday()):
            token = create_user().reset_password_token()

        response = self.client.get(f"{self.endpoint}/{token}")

        assert response.status == "422 UNPROCESSABLE ENTITY"
        assert response.json == {"message": "Expired token"}

    def test_request_with_valid_token(self, create_user):
        user = create_user()
        response = self.client.get(f"{self.endpoint}/{user.reset_password_token()}")

        assert response.status == "200 OK"
        assert response.json == {"message": "Valid token", "user_id": user.id}
