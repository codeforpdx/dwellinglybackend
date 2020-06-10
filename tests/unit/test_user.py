def test_admin_user(admin_user):
    assert admin_user.email == "user1@dwellingly.org"
    assert admin_user.role == "admin"
