adminUserEmail = "user1@dwellingly.org"
adminRole = "admin"

def test_admin_user():
    """The properties that match those sent to the user model by the fixture 'admin_user'."""
    adminUser = UserModel(email=adminUserEmail, password=userPassword, firstName="user1", lastName="admin", role=adminRole, archived=0)
    assert admin_user.email == adminUserEmail
    assert admin_user.role == adminRole
