from models.user import UserModel

def test_user_auth(client, admin_logged_in, admin_user):
    assert admin_logged_in.status_code == 200
    assert admin_logged_in.content_type == "application/json"
    assert "access_token" in admin_logged_in.json.keys()

    responseBadPassword = client.post("/api/login", json={"email": admin_user.email, "password": "incorrect"})
    assert responseBadPassword.status_code == 401

    responseMissingToken = client.get(f"/api/user/1", headers={})
    assert responseMissingToken.status_code == 401

def test_register_duplicate_user(client, admin_logged_in):
    duplicateUser = {
        "firstName": "first",
        "lastName": "last",
        "password": "1234",
        "email": "email@mail.com"
    }
    response = client.post("/api/register", json=duplicateUser)
    assert response.status_code == 201

    responseDuplicate = client.post("/api/register", json=duplicateUser)
    assert responseDuplicate.status_code == 400

def test_refresh_user(client, admin_logged_in):
    refreshHeader = {"Authorization": f"Bearer {admin_logged_in.json['refresh_token']}"}
    responseRefreshToken = client.post("api/refresh", json={}, headers=refreshHeader)
    assert responseRefreshToken.status_code == 200

def test_get_user_by_id(client, admin_logged_in, admin_auth_header, admin_user):
    user = UserModel.find_by_email(admin_user.email)
    response = client.get(f"/api/user/{user.id}", headers=admin_auth_header)
    assert response.status_code == 200

    responseBadUserId = client.get("/api/user/000000", headers=admin_auth_header)
    assert responseBadUserId.status_code == 404

def test_user_roles(client, admin_logged_in, admin_auth_header, admin_user):
    response = client.post("/api/users/role", json={"userrole": "admin"}, headers=admin_auth_header)
    assert response.status_code == 200

def test_archive_user(client, admin_logged_in, admin_auth_header, new_user):
    userToArchive = UserModel.find_by_email(new_user.email)
    response = client.post(f"/api/user/archive/{userToArchive.id}", json={}, headers=admin_auth_header)
    assert response.status_code == 201
    assert response.json["archived"] == True

    data = {
        "email": new_user.email,
        "password": new_user.password
    }
    responseLoginArchivedUser = client.post("/api/login", json=data)
    assert responseLoginArchivedUser.status_code == 403

def test_archive_user_failure(client, admin_logged_in, admin_auth_header):
    responseInvalidId = client.post("/api/user/archive/999999", json={}, headers=admin_auth_header)
    assert responseInvalidId.status_code == 400

def test_patch_user(client, admin_logged_in, admin_auth_header, new_user):
    userToPatch = UserModel.find_by_email(new_user.email)
    response = client.patch(f"/api/user/{userToPatch.id}", json={"role": "property_manager"}, headers=admin_auth_header)
    assert response.status_code == 201
    assert response.json["role"] == "property_manager"

    responseInvalidId = client.patch("/api/user/999999", json={"role": "new_role"}, headers=admin_auth_header)
    assert responseInvalidId.status_code == 400

def test_delete_user(client, admin_logged_in, admin_auth_header, new_user):
    userToDelete = UserModel.find_by_email(new_user.email)
    response = client.delete(f"/api/user/{userToDelete.id}", headers=admin_auth_header)
    assert response.status_code == 200

    responseInvalidId = client.delete("/api/user/999999", headers=admin_auth_header)
    assert responseInvalidId.status_code == 400
