import pytest
from conftest import is_valid
from models.user import RoleEnum
from flask_jwt_extended import create_access_token, create_refresh_token


@pytest.mark.usefixtures("client_class", "empty_test_db")
class TestUserAuthorization:
    def test_user_auth(self, create_admin_user):
        password = "strongestpasswordever"
        admin = create_admin_user(pw=password)
        login_response = self.client.post(
            "/api/login",
            json={"email": admin.email, "password": password},
        )
        """When an admin user logs in, the request should succeed."""
        assert is_valid(login_response, 200)  # OK
        assert "access_token" in login_response.json.keys()

        """
        The server responds with an error when a user attempts to login
        to an account without a valid role
        """
        admin.role = None
        responseBadPassword = self.client.post(
            "/api/login",
            json={"email": admin.email, "password": password},
        )
        assert responseBadPassword.status_code == 403
        assert responseBadPassword.json == {"message": "Invalid user"}
        admin.role = RoleEnum.ADMIN
        """
        The server responds with an error when a user attempts to
        login with an incorrect password.
        """
        responseBadPassword = self.client.post(
            "/api/login", json={"email": admin.email, "password": "incorrect"}
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

    def test_get_user(self, pm_header):

        """Non-admin requests return a 401 status code"""

        unauthorized_user_response = self.client.get(
            f"api/user?r={RoleEnum.PROPERTY_MANAGER.value}", headers=pm_header()
        )
        assert is_valid(unauthorized_user_response, 401)


@pytest.mark.usefixtures("client_class", "empty_test_db")
class TestUserDeleteAuthorization:
    def test_admin_is_authorized(self, admin_header, create_user):
        response = self.client.delete(
            f"/api/user/{create_user().id}", headers=admin_header
        )
        assert response.status_code == 200

    def test_join_staff_is_not_authorized(self, staff_header, create_user):
        response = self.client.delete(
            f"/api/user/{create_user().id}", headers=staff_header()
        )
        assert response.status_code == 401

    def test_pm_is_not_authorized(self, pm_header, create_user):
        response = self.client.delete(
            f"/api/user/{create_user().id}", headers=pm_header()
        )
        assert response.status_code == 401


@pytest.mark.usefixtures("client_class", "empty_test_db")
class TestUserPatchAuthorization:
    def test_auth_token_is_required(self):
        response = self.client.patch("api/user/5", json={})
        assert response.status_code == 401

    def test_admin_is_authorized_to_update_anyone(self, admin_header, create_user):
        response = self.client.patch(
            f"api/user/{create_user().id}", json={}, headers=admin_header
        )
        assert response == 200

    def test_staff_is_not_authorized_to_update_anyone(self, staff_header, create_user):
        response = self.client.patch(
            f"api/user/{create_user().id}", json={}, headers=staff_header()
        )
        assert response == 403

    def test_pm_is_not_authorized_to_update_anyone(self, pm_header, create_user):
        response = self.client.patch(
            f"api/user/{create_user().id}", json={}, headers=pm_header()
        )
        assert response == 403

    def test_staff_is_authorized_to_update_themselves(
        self, staff_header, create_join_staff
    ):
        staff = create_join_staff()
        response = self.client.patch(
            f"api/user/{staff.id}", json={}, headers=staff_header(staff)
        )
        assert response == 200

    def test_pm_is_authorized_to_update_themselves(
        self, pm_header, create_property_manager
    ):
        pm = create_property_manager()
        response = self.client.patch(
            f"api/user/{pm.id}", json={}, headers=pm_header(pm)
        )
        assert response == 200


@pytest.mark.usefixtures("client_class", "empty_test_db")
class TestUserLogic:
    # TODO: This doesn't belong in auth tests
    def test_password(self, header, create_user, faker):
        """
        The server responds with a 401 if a patch for a pw reset is made
        and the current pw does not match the pw in the db
        """
        password = "strongestpasswordever"
        user = create_user(pw=password)
        new_password = faker.password()
        responseInvalidCurrentPassword = self.client.patch(
            f"api/user/{user.id}",
            json={
                "current_password": "askdjf",
                "new_password": new_password,
                "confirm_password": new_password,
            },
            headers=header(user),
        )
        assert responseInvalidCurrentPassword.status_code == 401

        """
        The server responds with a 422 if a patch for a pw reset is made
        and the current pw matches but the new and confirm pw does not
        """
        responseInvalidConfirmPassword = self.client.patch(
            f"api/user/{user.id}",
            json={
                "current_password": password,
                "new_password": new_password,
                "confirm_password": f"{new_password}oops",
            },
            headers=header(user),
        )
        assert responseInvalidConfirmPassword.status_code == 422

        """
        The server responds with a 201 if a patch for a pw reset is made
        and the current pw matches the pw in the db
        """
        new_password = "new password"
        responseValidCurrentPassword = self.client.patch(
            f"api/user/{user.id}",
            json={
                "current_password": password,
                "new_password": new_password,
                "confirm_password": new_password,
            },
            headers=header(user),
        )
        assert responseValidCurrentPassword.status_code == 200

    # TODO: this doesn't belong in auth tests.
    def test_jwt_refresh(self, header, create_user):
        """
        The server responds with updated user information
        and a new jwt token when a user patches his own information
        """

        user = create_user()
        original_access_token = create_access_token(identity=user.id, fresh=True)
        original_refresh_token = create_refresh_token(user.id)

        newPhone = "555-555-5555"

        response = self.client.patch(
            f"/api/user/{user.id}",
            json={"phone": newPhone},
            headers=header(user),
        )

        new_access_token = response.json["access_token"]
        new_refresh_token = response.json["refresh_token"]

        assert newPhone == response.json["phone"]
        assert original_access_token != new_access_token
        assert original_refresh_token != new_refresh_token

        """Non-Admin users cannot change their own role"""
        user = create_user(admin=False)
        response = self.client.patch(
            f"/api/user/{user.id}",
            json={"role": RoleEnum.ADMIN.value},
            headers=header(user),
        )

        assert response.status_code == 403
        assert response.json == {"message": "Not Authorized"}
