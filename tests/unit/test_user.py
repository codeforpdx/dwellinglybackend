def test_new_user(new_user):
    assert new_user.email == "user1@dwellingly.org"
    assert new_user.role == "admin"
