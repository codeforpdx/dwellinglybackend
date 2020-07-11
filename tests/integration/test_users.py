from models.user import UserModel
from conftest import login_user

def test_user_auth(client, test_database, admin_user):
    login_response, auth_header = login_user(client, admin_user)
    """When an admin user logs in, the request should succeed."""
    assert login_response.status_code == 200
    assert login_response.content_type == "application/json"
    assert "access_token" in login_response.json.keys()

    """The server responds with an error when a user attempts to login with an incorrect password."""
    responseBadPassword = client.post("/api/login", json={"email": admin_user.email, "password": "incorrect"})
    assert responseBadPassword.status_code == 401

    """The server responds with an error when a request is made (to a protected route) without the admin token provided."""
    responseMissingToken = client.get(f"/api/user/1", headers={})
    assert responseMissingToken.status_code == 401

def test_register_duplicate_user(client, test_database):
    """When a user first registers, the server responds successfully."""
    genericUser = {
        "firstName": "first",
        "lastName": "last",
        "password": "1234",
        "email": "email@mail.com"
    }
    login_response = client.post("/api/register", json=genericUser)
    assert login_response.status_code == 201

    """The server responds with an error if duplicate user details are used for registration."""
    duplicateUser = genericUser
    responseDuplicate = client.post("/api/register", json=duplicateUser)
    assert responseDuplicate.status_code == 400

def test_refresh_user(client, test_database, admin_user):
    login_response, auth_header = login_user(client, admin_user)
    """The refresh route returns a successful response code."""
    refreshHeader = {"Authorization": f"Bearer {login_response.json['refresh_token']}"}
    responseRefreshToken = client.post("api/refresh", json={}, headers=refreshHeader)
    assert responseRefreshToken.status_code == 200

def test_get_user_by_id(client, test_database, admin_user):
    login_response, auth_header = login_user(client, admin_user)

    """The get user by id route returns a successful response code."""
    user = UserModel.find_by_email(admin_user.email)
    response = client.get(f"/api/user/{user.id}", headers=auth_header)
    assert response.status_code == 200

    """The server responds with an error if a non-existent user id is requested from the get user by id route."""
    responseBadUserId = client.get("/api/user/000000", headers=auth_header)
    assert responseBadUserId.status_code == 404

def test_user_roles(client, test_database, admin_user):
    """The get users by role route returns a successful response code."""
    login_response, auth_header = login_user(client, admin_user)
    response = client.post("/api/users/role", json={"userrole": "admin"}, headers=auth_header)
    assert response.status_code == 200

def test_archive_user(client, test_database, new_user, admin_user):
    """The archive user by id route returns a successful response code and changes the user's status."""
    admin_login_response, admin_auth_header = login_user(client, admin_user)
    userToArchive = UserModel.find_by_email(new_user.email)
    response = client.post(f"/api/user/archive/{userToArchive.id}", json={}, headers=admin_auth_header)
    assert response.status_code == 201
    assert response.json["archived"] == True

    """An archived user is prevented from logging in."""
    data = {
        "email": new_user.email,
        "password": new_user.password
    }
    responseLoginArchivedUser = client.post("/api/login", json=data)
    assert responseLoginArchivedUser.status_code == 403

def test_archive_user_failure(client, test_database, admin_user):
    """The server responds with an error if a non-existent user id is used for the archive user by id route."""
    login_response, auth_header = login_user(client, admin_user)
    responseInvalidId = client.post("/api/user/archive/999999", json={}, headers=auth_header)
    assert responseInvalidId.status_code == 400

def test_patch_user(client, test_database, admin_user, new_user):
    """The route to patch a user by id returns a successful response code and the expected data is patched."""
    admin_login_response, admin_auth_header = login_user(client, admin_user)
    expected = "property_manager"
    userToPatch = UserModel.find_by_email(new_user.email)
    response = client.patch(f"/api/user/{userToPatch.id}", json={"role": expected}, headers=admin_auth_header)
    actual = response.json["role"]
    assert response.status_code == 201
    assert expected == actual

    """The server responds with an error if a non-existent user id is used for the patch user by id route."""
    responseInvalidId = client.patch("/api/user/999999", json={"role": "new_role"}, headers=admin_auth_header)
    assert responseInvalidId.status_code == 400

def test_delete_user(client, test_database, admin_user, property_manager_user, new_user):
    userToDelete = UserModel.find_by_email(new_user.email)

    """ Attempted User Delete as 'property-manager' should fail """
    pm_login_response, pm_auth_header = login_user(client, property_manager_user)
    response = client.delete(f"/api/user/{userToDelete.id}", headers=pm_auth_header)
    assert response.status_code == 401 # UNAUTHORIZED - Admin Access Required
    
    """ Attempted User Delete as 'pending' should fail """
    pending_login_response, pending_auth_header = login_user(client, new_user)
    response = client.delete(f"/api/user/{userToDelete.id}", headers=pending_auth_header)
    assert response.status_code == 401 # UNAUTHORIZED - Admin Access Required

    """ The route to delete a user by id returns a successful response code. """
    admin_login_response, admin_auth_header = login_user(client, admin_user)
    response = client.delete(f"/api/user/{userToDelete.id}", headers=admin_auth_header)
    assert response.status_code == 200

    """ The server responds with an error if a non-existent user id is used for the delete user by id route. """
    responseInvalidId = client.delete("/api/user/999999", headers=admin_auth_header)
    assert responseInvalidId.status_code == 400
