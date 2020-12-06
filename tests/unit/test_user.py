import pytest
from models.user import UserModel, RoleEnum
from unittest.mock import patch
import jwt
import time
from freezegun import freeze_time

@patch.object(jwt, 'encode')
def test_reset_password_token(stubbed_encode, app, test_database):
    user = UserModel.find_by_id(1)

    with freeze_time(time.ctime(time.time())):
        ten_minutes = time.time() + 600
        payload = {'user_id': user.id, 'exp': ten_minutes}

        assert user.reset_password_token()
        stubbed_encode.assert_called_once_with(payload, app.secret_key, algorithm='HS256')

def test_full_name(empty_test_db, create_admin_user):
    admin= create_admin_user(firstName='first', lastName='last')
    assert admin.full_name() == 'first last'


@pytest.mark.usefixtures("empty_test_db")
class TestFixtures:
    def test_create_admin_user(self, create_admin_user):
        admin = create_admin_user()
        assert admin
        assert admin.role == RoleEnum.ADMIN

        def test_multiple_admins_can_be_created():
            return create_admin_user()

        assert test_multiple_admins_can_be_created()

    def test_create_join_staff(self, create_join_staff):
        staff = create_join_staff()
        assert staff
        assert staff.role == RoleEnum.STAFF

        def test_multiple_join_staff_can_be_created():
            return create_join_staff()

        assert test_multiple_join_staff_can_be_created()

    def test_create_property_manager(self, create_property_manager):
        pm = create_property_manager()
        assert pm
        assert pm.role == RoleEnum.PROPERTY_MANAGER

        def test_multiple_pms_can_be_created():
            return create_property_manager()

        assert test_multiple_pms_can_be_created()

    def test_create_unauthorized_user(self, create_unauthorized_user):
        user = create_unauthorized_user()
        assert user.role == RoleEnum.PENDING

        def test_multiple_users_can_be_created():
            return create_unauthorized_user()

        assert test_multiple_users_can_be_created()
