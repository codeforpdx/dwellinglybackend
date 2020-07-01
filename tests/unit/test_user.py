from conftest import adminUserEmail
from conftest import adminRole

def test_admin_user(admin_user):
    """The properties that match those sent to the user model by the fixture 'admin_user'."""
    assert admin_user.email == adminUserEmail
    assert admin_user.role == adminRole
