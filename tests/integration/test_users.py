import pytest
from unittest.mock import patch
from models.user import UserModel
from models.users.admin import Admin
from schemas import UserRegisterSchema
from tests.schemas.test_user_schema import user_register_valid_payload
from conftest import is_valid
from freezegun import freeze_time
from models.user import RoleEnum
from utils.time import time_format


@pytest.mark.usefixtures("client_class", "empty_test_db")
class TestUserLogin:
    def setup(self):
        self.password = "strongestpasswordever"

    def test_last_active(self, create_admin_user):
        user = create_admin_user(pw=self.password)
        assert user.lastActive.strftime(time_format) != "01/01/2020 00:00:00"

        with freeze_time("2020-01-01"):
            self.client.post(
                "/api/login",
                json={"email": user.email, "password": self.password},
            )
            assert user.lastActive.strftime(time_format) == "01/01/2020 00:00:00"

    def test_refresh_user(self, create_admin_user):
        user = create_admin_user(pw=self.password)
        response = self.client.post(
            "/api/login", json={"email": user.email, "password": self.password}
        )
        """The refresh route returns a successful response code."""
        refreshHeader = {"Authorization": f"Bearer {response.json['refresh_token']}"}
        responseRefreshToken = self.client.post(
            "api/refresh", json={}, headers=refreshHeader
        )
        assert responseRefreshToken.status_code == 200


@pytest.mark.usefixtures("client_class", "empty_test_db")
class TestUserGet:
    def test_get(self, create_user, valid_header):
        user = create_user()
        with patch.object(UserModel, "find", return_value=user) as mock_find:
            response = self.client.get("/api/user/98734", headers=valid_header)

        mock_find.assert_called_once_with(98734)
        assert response.status_code == 200
        assert response.json == user.json()


@pytest.mark.usefixtures("client_class", "empty_test_db")
class TestUserDelete:
    def test_delete(self, create_user, valid_header):
        user = create_user()
        with patch.object(UserModel, "find", return_value=user) as mock_find:
            with patch.object(user, "delete_from_db") as mock_delete:
                response = self.client.delete("/api/user/9873", headers=valid_header)

        mock_find.assert_called_once_with(9873)
        mock_delete.assert_called()
        assert response.status_code == 200
        assert response.json == {"message": "User deleted"}

    def test_admin_cannot_delete_themselves(self, create_admin_user, header):
        admin = create_admin_user()
        response = self.client.delete(f"api/user/{admin.id}", headers=header(admin))
        assert is_valid(response, 400)


@pytest.mark.usefixtures("client_class", "empty_test_db")
class TestUsersGet:
    def test_get(self, create_admin_user, header):
        admin = create_admin_user()
        response = self.client.get(
            f"/api/user?r={RoleEnum.ADMIN.value}", headers=header(admin)
        )

        assert response.status_code == 200
        assert response.json == {"users": [admin.json()]}

        """Queries with a non-existing role returns a 400 response"""

        unknown_role = max(RoleEnum.get_values()) + 1
        unknown_user_response = self.client.get(
            f"api/user?r={unknown_role}", headers=header(admin)
        )
        assert is_valid(unknown_user_response, 400)


@pytest.mark.usefixtures("client_class", "empty_test_db")
class TestArchiveUser:
    def test_archive_user(self, create_user, valid_header, header):
        """
        The archive user by id route returns a successful response code
        and changes the user's status.
        """
        password = "strongestpasswordever"
        user = create_user(pw=password)
        response = self.client.post(
            f"/api/user/archive/{user.id}", json={}, headers=valid_header
        )
        assert response.status_code == 201
        assert response.json["archived"] is True

        # TODO: Make this pass! Issue codeforpdx/dwellingly-app/issues/660
        """An archived user should not have access"""
        # response = self.client.get("/api/lease", json={}, headers=header(user))
        # assert response.status_code == 403

        """An archived user is prevented from logging in."""
        data = {"email": user.email, "password": password}
        response = self.client.post("/api/login", json=data)
        assert response.status_code == 403
        assert response.json == {"message": "Invalid user"}

        """Admin user attempting to archive themselves should get error"""
        admin = Admin.query.first()
        response = self.client.post(
            f"/api/user/archive/{admin.id}", json={}, headers=valid_header
        )
        assert response.status_code == 400
        assert response.json == {"message": "Cannot archive self"}


@pytest.mark.usefixtures("client_class", "empty_test_db")
class TestUser:
    def test_role_update(self, valid_header, create_unauthorized_user):
        id = create_unauthorized_user().id
        payload = {"role": RoleEnum.ADMIN.value}
        self.client.patch(f"api/user/{id}", json=payload, headers=valid_header)

        user = Admin.find(id)
        assert user.role == RoleEnum.ADMIN
        assert user.type == "admin"


@pytest.mark.usefixtures("client_class", "empty_test_db")
class TestRegisterUser:
    def setup(self):
        self.endpoint = "/api/register"
        self.valid_payload = user_register_valid_payload

    def test_user_can_register_with_valid_payload(self, user_attributes):
        response = self.client.post(
            self.endpoint, json=self.valid_payload(user_attributes())
        )

        assert response.status_code == 201

    @patch.object(UserModel, "create")
    def test_user_calls_create(self, mock_create, user_attributes):
        payload = self.valid_payload(user_attributes())

        self.client.post(self.endpoint, json=payload)

        mock_create.assert_called_with(schema=UserRegisterSchema, payload=payload)
