import pytest
from unittest.mock import patch
from models.user import UserModel
from schemas import UserRegisterSchema
from tests.schemas.test_user_schema import user_register_valid_payload
from conftest import is_valid
from freezegun import freeze_time
from models.user import RoleEnum
from utils.time import time_format

plaintext_password = "1234"
new_password = "newPassword"


def test_last_active(client, test_database, admin_user):
    user = UserModel.find_by_email(admin_user.email)
    assert user.lastActive.strftime(time_format) != "01/01/2020 00:00:00"

    with freeze_time("2020-01-01"):
        client.post(
            "/api/login",
            json={"email": admin_user.email, "password": plaintext_password},
        )
        user = UserModel.find_by_email(admin_user.email)
        assert user.lastActive.strftime(time_format) == "01/01/2020 00:00:00"


def test_refresh_user(client, test_database, admin_user):
    login_response = client.post(
        "/api/login", json={"email": admin_user.email, "password": plaintext_password}
    )
    """The refresh route returns a successful response code."""
    refreshHeader = {"Authorization": f"Bearer {login_response.json['refresh_token']}"}
    responseRefreshToken = client.post("api/refresh", json={}, headers=refreshHeader)
    assert responseRefreshToken.status_code == 200


def test_get_user_by_id(client, empty_test_db, create_admin_user, valid_header):
    """The get user by id route returns a successful response code."""
    user = create_admin_user()
    response = client.get(f"/api/user/{user.id}", headers=valid_header)
    assert response.status_code == 200

    """
    The server responds with an error if a non-existent user id
    is requested from the get user by id route.
    """
    responseBadUserId = client.get("/api/user/000000", headers=valid_header)
    assert responseBadUserId.status_code == 404
    assert responseBadUserId.json == {"message": "User not found"}


def test_get_pm_by_id(
    client,
    empty_test_db,
    create_property_manager,
    create_property,
    create_lease,
    valid_header,
):
    user = create_property_manager()
    prop = create_property(manager_ids=[user.id])
    lease_1 = create_lease(property=prop)
    lease_2 = create_lease(property=prop)

    response = client.get(f"/api/user/{user.id}", headers=valid_header)

    property_list = response.json["properties"]
    tenants_list = response.json["tenants"]

    """
    The get user by id route returns a successful response code
    when the queried user is a property manager
    """
    assert response.status_code == 200

    """The PM's properties are returned as a list of JSON objects"""
    assert property_list == [prop.json()]

    """
    Tenants are retreived through the leases on each
    property and returned as a list of JSON objects
    """
    assert tenants_list == [lease_1.tenant.json(), lease_2.tenant.json()]


def test_user_roles(client, auth_headers):
    """The get users by role route returns a successful response code."""
    response = client.post(
        "/api/users/role",
        json={"userrole": RoleEnum.ADMIN.value},
        headers=auth_headers["admin"],
    )
    assert len(response.get_json()["users"]) == 4
    assert response.status_code == 200

    """The get users by role route returns only property managers."""
    response = client.post(
        "/api/users/role",
        json={"userrole": RoleEnum.PROPERTY_MANAGER.value},
        headers=auth_headers["admin"],
    )
    managers = response.get_json()["users"]
    assert len(managers) == 3
    assert all([RoleEnum.PROPERTY_MANAGER.value == pm["role"] for pm in managers])
    assert response.status_code == 200

    """The get users by role route returns only property managers named Gray Pouponn."""
    response = client.post(
        "/api/users/role",
        json={"name": "ray", "userrole": RoleEnum.PROPERTY_MANAGER.value},
        headers=auth_headers["admin"],
    )
    managers = response.get_json()["users"]
    assert len(managers) == 1
    assert all(["Gray" == pm["firstName"] for pm in managers])
    assert all(["Pouponn" == pm["lastName"] for pm in managers])
    assert response.status_code == 200

    """The get users by role route returns zero users when no names match."""
    response = client.post(
        "/api/users/role",
        json={"name": "ABCDEFG", "userrole": RoleEnum.PROPERTY_MANAGER.value},
        headers=auth_headers["admin"],
    )
    managers = response.get_json()["users"]
    assert len(managers) == 0
    assert response.status_code == 200


def test_archive_user(client, auth_headers, new_user, admin_user):
    """
    The archive user by id route returns a successful response code
    and changes the user's status.
    """
    userToArchive = UserModel.find_by_email(new_user.email)
    response = client.post(
        f"/api/user/archive/{userToArchive.id}", json={}, headers=auth_headers["admin"]
    )
    assert response.status_code == 201
    assert response.json["archived"] is True

    """An archived user is prevented from logging in."""
    data = {"email": new_user.email, "password": plaintext_password}
    responseLoginArchivedUser = client.post("/api/login", json=data)
    assert responseLoginArchivedUser.status_code == 403
    assert responseLoginArchivedUser.json == {"message": "Invalid user"}

    """Admin user attempting to archive themselves should get error"""
    response = client.post(
        f"/api/user/archive/{admin_user.id}", json={}, headers=auth_headers["admin"]
    )
    assert response.status_code == 400
    assert response.json == {"message": "Cannot archive self"}


def test_unique_user_constraint(client, auth_headers, new_user):
    """Emails must be unique, otherwise an Exception is thrown"""
    with pytest.raises(Exception):
        userToPatch = UserModel.find_by_email(new_user.email)
        client.patch(
            f"/api/user/{userToPatch.id}",
            json={"email": "user1@dwellingly.org"},
            headers=auth_headers["admin"],
        )


def test_delete_user(client, auth_headers, new_user, admin_user):
    userToDelete = UserModel.find_by_email(new_user.email)

    response = client.delete(
        f"/api/user/{userToDelete.id}", headers=auth_headers["admin"]
    )
    assert is_valid(response, 200)  # OK

    response = client.delete(f"api/user/{admin_user.id}", headers=auth_headers["admin"])
    assert is_valid(response, 400)


def test_get_user(client, auth_headers, new_user):
    """GET '/user' returns a list of all users queried by role"""

    admin_user_response = client.get(
        f"/api/user?r={RoleEnum.ADMIN.value}", headers=auth_headers["admin"]
    )

    assert is_valid(admin_user_response, 200)
    assert all(
        admin["role"] == RoleEnum.ADMIN.value
        for admin in admin_user_response.json["users"]
    )

    """Queries with a non-existing role returns a 400 response"""

    unknown_role = max(RoleEnum.get_values()) + 1
    unknown_user_response = client.get(
        f"api/user?r={unknown_role}", headers=auth_headers["admin"]
    )
    assert is_valid(unknown_user_response, 400)


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
