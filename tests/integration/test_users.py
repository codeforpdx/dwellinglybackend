import pytest
from unittest.mock import patch
from models.user import UserModel
from schemas import UserRegisterSchema
from tests.schemas.test_user_schema import user_register_valid_payload
from conftest import is_valid
from freezegun import freeze_time
from models.user import RoleEnum
from flask_jwt_extended import create_access_token, create_refresh_token
from utils.time import time_format

plaintext_password = "1234"
new_password = "newPassword"


def test_user_auth(client, test_database, admin_user):
    login_response = client.post(
        "/api/login", json={"email": admin_user.email, "password": plaintext_password}
    )
    """When an admin user logs in, the request should succeed."""
    assert is_valid(login_response, 200)  # OK
    assert "access_token" in login_response.json.keys()

    """
    The server responds with an error when a user attempts to login
    to an account without a valid role
    """
    admin_user.role = None
    responseBadPassword = client.post(
        "/api/login", json={"email": admin_user.email, "password": plaintext_password}
    )
    assert responseBadPassword.status_code == 403
    assert responseBadPassword.json == {"message": "Invalid user"}
    admin_user.role = RoleEnum.ADMIN
    """
    The server responds with an error when a user attempts to
    login with an incorrect password.
    """
    responseBadPassword = client.post(
        "/api/login", json={"email": admin_user.email, "password": "incorrect"}
    )
    assert responseBadPassword.status_code == 401
    assert responseBadPassword.json == {"message": "Invalid credentials"}

    """
    The server responds with an error when a request is made (to a protected route)
    without the admin token provided.
    """
    responseMissingToken = client.get("/api/user/1", headers={})
    assert responseMissingToken.status_code == 401
    assert responseMissingToken.json == {"message": "Missing authorization header"}


def test_bad_user_auth(client, test_database):
    login_response = client.post(
        "/api/login", json={"email": "bad@user.com", "password": "pass"}
    )
    assert login_response.status_code == 401


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


def test_get_user_by_id(client, auth_headers, admin_user):
    """The get user by id route returns a successful response code."""
    user = UserModel.find_by_email(admin_user.email)
    response = client.get(f"/api/user/{user.id}", headers=auth_headers["admin"])
    assert response.status_code == 200

    """
    The server responds with an error if a non-existent user id
    is requested from the get user by id route.
    """
    responseBadUserId = client.get("/api/user/000000", headers=auth_headers["admin"])
    assert responseBadUserId.status_code == 404
    assert responseBadUserId.json == {"message": "User not found"}


def test_user_roles(client, auth_headers):
    """The get users by role route returns a successful response code."""
    response = client.post(
        "/api/users/role",
        json={"userrole": RoleEnum.ADMIN.value},
        headers=auth_headers["admin"],
    )
    print("Admin users json: {}".format(response.get_json()["users"]))
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


def test_user_no_roles(client, auth_headers):
    pass


def test_archive_user(client, auth_headers, new_user):
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


def test_archive_user_failure(client, auth_headers):
    """
    The server responds with an error if a non-existent user id
    is used for the archive user by id route.
    """
    responseInvalidId = client.post(
        "/api/user/archive/999999", json={}, headers=auth_headers["admin"]
    )
    assert responseInvalidId.status_code == 400
    assert responseInvalidId.json == {"message": "User cannot be archived"}


def test_patch_user(
    client, auth_headers, property_manager_user, create_admin_user, pm_header
):
    """
    The route to patch a user by id returns a successful response code
    and the expected data is patched.
    """

    payload = {
        "role": RoleEnum.PROPERTY_MANAGER.value,
        "email": "patch@test.com",
        "phone": "503-867-5309",
    }

    userToPatch = UserModel.find_by_email(property_manager_user.email)
    response = client.patch(
        f"/api/user/{create_admin_user().id}",
        json=payload,
        headers=auth_headers["admin"],
    )

    actualRole = int(response.json["role"])
    actualEmail = response.json["email"]
    actualPhone = response.json["phone"]

    assert response.status_code == 201
    assert payload["role"] == actualRole
    assert payload["email"] == actualEmail
    assert payload["phone"] == actualPhone

    """
    The server responds with a 401 if a patch for a pw reset is made
    and the current pw does not match the pw in the db
    """
    responseInvalidCurrentPassword = client.patch(
        f"api/user/{userToPatch.id}",
        json={
            "current_password": "incorrect",
            "new_password": new_password,
            "confirm_password": new_password,
        },
        headers=auth_headers["admin"],
    )
    assert responseInvalidCurrentPassword.status_code == 401

    """
    The server responds with a 422 if a patch for a pw reset is made
    and the current pw matches but the new and confirm pw does not
    """
    responseInvalidConfirmPassword = client.patch(
        f"api/user/{userToPatch.id}",
        json={
            "current_password": plaintext_password,
            "new_password": new_password,
            "confirm_password": "not_new_password",
        },
        headers=auth_headers["admin"],
    )
    assert responseInvalidConfirmPassword.status_code == 422

    """
    The server responds with a 201 if a patch for a pw reset is made
    and the current pw matches the pw in the db
    """
    responseValidCurrentPassword = client.patch(
        f"api/user/{userToPatch.id}",
        json={
            "current_password": plaintext_password,
            "new_password": new_password,
            "confirm_password": new_password,
        },
        headers=auth_headers["admin"],
    )
    assert responseValidCurrentPassword.status_code == 201

    """
    The server responds with an error if a non-existent user id
    is used for the patch user by id route.
    """
    responseInvalidId = client.patch(
        "/api/user/999999", json={"role": "new_role"}, headers=auth_headers["admin"]
    )
    assert responseInvalidId.status_code == 400

    """
    The server responds with a 403 error if a non-admin
    attempts to edit another user's information
    """

    newEmail = "unauthorizedpatch@test.com"

    unauthorizedResponse = client.patch(
        f"/api/user/{userToPatch.id}", json={"email": newEmail}, headers=pm_header
    )

    assert unauthorizedResponse.status_code == 403

    """
    The server responds with updated user information
    and a new jwt token when a user patches his own information
    """

    original_access_token = create_access_token(identity=userToPatch.id, fresh=True)
    original_refresh_token = create_refresh_token(userToPatch.id)

    newPhone = "555-555-5555"

    tokenTestResponse = client.patch(
        f"/api/user/{userToPatch.id}",
        json={"phone": newPhone},
        headers={"Authorization": f"Bearer {original_access_token}"},
    )

    new_access_token = tokenTestResponse.json["access_token"]
    new_refresh_token = tokenTestResponse.json["refresh_token"]

    assert newPhone == tokenTestResponse.json["phone"]
    assert original_access_token != new_access_token
    assert original_refresh_token != new_refresh_token

    """Non-Admin users cannot change their own role"""

    newRole = RoleEnum.ADMIN.value

    changeOwnRoleResponse = client.patch(
        f"/api/user/{userToPatch.id}",
        json={"role": newRole},
        headers={"Authorization": f"Bearer {new_access_token}"},
    )

    assert changeOwnRoleResponse.status_code == 403
    assert changeOwnRoleResponse.json == {"message": "Only admins can change roles"}


def test_unique_user_constraint(client, auth_headers, new_user):
    """Emails must be unique, otherwise an Exception is thrown"""
    with pytest.raises(Exception):
        userToPatch = UserModel.find_by_email(new_user.email)
        client.patch(
            f"/api/user/{userToPatch.id}",
            json={"email": "user1@dwellingly.org"},
            headers=auth_headers["admin"],
        )


def test_delete_user(client, auth_headers, new_user):
    userToDelete = UserModel.find_by_email(new_user.email)

    response = client.delete(f"/api/user/{userToDelete.id}", headers=auth_headers["pm"])
    assert is_valid(response, 401)  # UNAUTHORIZED - Admin Access Required

    response = client.delete(
        f"/api/user/{userToDelete.id}", headers=auth_headers["pending"]
    )
    assert is_valid(response, 401)  # UNAUTHORIZED - Admin Access Required

    response = client.delete(
        f"/api/user/{userToDelete.id}", headers=auth_headers["admin"]
    )
    assert is_valid(response, 200)  # OK

    response = client.delete("/api/user/999999", headers=auth_headers["admin"])
    assert is_valid(response, 400)  # BAD REQUEST


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

    """Non-admin requests return a 401 status code"""

    unauthorized_user_response = client.get(
        f"api/user?r={RoleEnum.PROPERTY_MANAGER.value}", headers=auth_headers["pm"]
    )
    assert is_valid(unauthorized_user_response, 401)


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
