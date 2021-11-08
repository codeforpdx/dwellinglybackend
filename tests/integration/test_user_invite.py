import pytest
from models.user import RoleEnum
from unittest.mock import patch
from resources.email import Email


@pytest.mark.usefixtures("client_class")
class TestUserInvite:
    def setup(self):
        self.endpoint = "/api/user/invite"

    @patch.object(Email, "send_user_invite_msg")
    def test_invite_user(self, send_user_invite_msg, valid_header, user_attributes):
        response = self.client.post(
            self.endpoint,
            headers=valid_header,
            json=user_attributes(role=RoleEnum.STAFF.value),
        )

        send_user_invite_msg.assert_called()
        assert response.status_code == 201
        assert response.json == {"message": "User Invited"}
