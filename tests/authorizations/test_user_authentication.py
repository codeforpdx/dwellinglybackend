import pytest
from conftest import is_valid
from models.user import RoleEnum, UserModel
from flask_jwt_extended import create_access_token, create_refresh_token


@pytest.mark.usefixtures("client_class", "empty_test_db")
class TestUserAuthentication:
    def setup(self):
        self.plaintext_password = "1234"
        self.new_password = "newPassword"

    def test_user_auth(self, test_database, admin_user):
        login_response = self.client.post(
            "/api/login",
            json={"email": admin_user.email, "password": self.plaintext_password},
        )
        """When an admin user logs in, the request should succeed."""
        assert is_valid(login_response, 200)  # OK
        assert "access_token" in login_response.json.keys()

        """
        The server responds with an error when a user attempts to login
        to an account without a valid role
        """
        admin_user.role = None
        responseBadPassword = self.client.post(
            "/api/login",
            json={"email": admin_user.email, "password": self.plaintext_password},
        )
        assert responseBadPassword.status_code == 403
        assert responseBadPassword.json == {"message": "Invalid user"}
        admin_user.role = RoleEnum.ADMIN
        """
        The server responds with an error when a user attempts to
        login with an incorrect password.
        """
        responseBadPassword = self.client.post(
            "/api/login", json={"email": admin_user.email, "password": "incorrect"}
        )
        assert responseBadPassword.status_code == 401
        assert responseBadPassword.json == {"message": "Invalid credentials"}

        """
        The server responds with an error when a request is made (to a protected route)
        without the admin token provided.
        """
        responseMissingToken = self.client.get("/api/user/1", headers={})
        assert responseMissingToken.status_code == 401
        assert responseMissingToken.json == {"message": "Missing authorization header"}

    def test_bad_user_auth(self):
        login_response = self.client.post(
            "/api/login", json={"email": "bad@user.com", "password": "pass"}
        )
        assert login_response.status_code == 401

    def test_patch_user(
        self, auth_headers, property_manager_user, create_admin_user, pm_header
    ):

        payload = {
            "role": RoleEnum.PROPERTY_MANAGER.value,
            "email": "patch@test.com",
            "phone": "503-867-5309",
        }

        userToPatch = UserModel.find_by_email(property_manager_user.email)

        """
        The server responds with a 401 if a patch for a pw reset is made
        and the current pw does not match the pw in the db
        """
        responseInvalidCurrentPassword = self.client.patch(
            f"api/user/{userToPatch.id}",
            json={
                "current_password": "incorrect",
                "new_password": self.new_password,
                "confirm_password": self.new_password,
            },
            headers=auth_headers["admin"],
        )
        assert responseInvalidCurrentPassword.status_code == 401

        """
        The server responds with a 422 if a patch for a pw reset is made
        and the current pw matches but the new and confirm pw does not
        """
        responseInvalidConfirmPassword = self.client.patch(
            f"api/user/{userToPatch.id}",
            json={
                "current_password": self.plaintext_password,
                "new_password": self.new_password,
                "confirm_password": "not_new_password",
            },
            headers=auth_headers["admin"],
        )
        assert responseInvalidConfirmPassword.status_code == 422

        """
        The server responds with a 201 if a patch for a pw reset is made
        and the current pw matches the pw in the db
        """
        responseValidCurrentPassword = self.client.patch(
            f"api/user/{userToPatch.id}",
            json={
                "current_password": self.plaintext_password,
                "new_password": self.new_password,
                "confirm_password": self.new_password,
            },
            headers=auth_headers["admin"],
        )
        assert responseValidCurrentPassword.status_code == 201

        """
        The server responds with a 403 error if a non-admin
        attempts to edit another user's information
        """

        newEmail = "unauthorizedpatch@test.com"

        unauthorizedResponse = self.client.patch(
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

        tokenTestResponse = self.client.patch(
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

        changeOwnRoleResponse = self.client.patch(
            f"/api/user/{userToPatch.id}",
            json={"role": newRole},
            headers={"Authorization": f"Bearer {new_access_token}"},
        )

        assert changeOwnRoleResponse.status_code == 403
        assert changeOwnRoleResponse.json == {"message": "Only admins can change roles"}

    def test_delete_user(self, auth_headers, new_user):
        userToDelete = UserModel.find_by_email(new_user.email)

        response = self.client.delete(
            f"/api/user/{userToDelete.id}", headers=auth_headers["pm"]
        )
        assert is_valid(response, 401)  # UNAUTHORIZED - Admin Access Required

    def test_get_user(self, auth_headers):

        """Non-admin requests return a 401 status code"""

        unauthorized_user_response = self.client.get(
            f"api/user?r={RoleEnum.PROPERTY_MANAGER.value}", headers=auth_headers["pm"]
        )
        assert is_valid(unauthorized_user_response, 401)
