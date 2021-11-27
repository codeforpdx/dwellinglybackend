import pytest
from unittest.mock import patch

from models.user import RoleEnum
from resources.email import Email
from models.users.property_manager import PropertyManager
from schemas.user import PropertyManagerSchema


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


@pytest.mark.usefixtures("client_class")
class TestPropertyManagerInvite:
    def setup(self):
        self.endpoint = "/api/user/invite/property_manager"

    @patch.object(Email, "send_user_invite_msg")
    def test_invite_property_manager(
        self, send_user_invite_msg, user_attributes, valid_header
    ):
        payload = user_attributes()

        with patch.object(PropertyManager, "create") as mock_create_pm:
            response = self.client.post(
                self.endpoint,
                headers=valid_header,
                json=payload,
            )

        send_user_invite_msg.assert_called()
        mock_create_pm.assert_called_once_with(
            schema=PropertyManagerSchema, payload=payload
        )

        assert response.status_code == 201
        assert response.json == {"message": "Property Manager Invited"}
