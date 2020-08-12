from models.user import UserModel

adminUserEmail = "user1@dwellingly.org"
adminRole = "admin"
phone = "1 800-Cal-Saul"

def test_admin_user():
    """The properties must match the model's inputs."""
    admin_user = UserModel(email=adminUserEmail, password="1234", firstName="user1", lastName="admin", phone=phone, role=adminRole, archived=0)
    assert admin_user.email == adminUserEmail
    assert admin_user.role == adminRole
    assert admin_user.phone == phone
