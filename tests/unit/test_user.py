import pytest
import jwt
import time
from unittest.mock import patch
from models.user import UserModel
from schemas.user import UserSchema
from freezegun import freeze_time
from tests.unit.base_interface_test import BaseInterfaceTest


class TestUserModel(BaseInterfaceTest):
    def setup(self):
        self.object = UserModel(password="1234")
        self.schema = UserSchema
        self.custom_404_msg = "User not found"


@pytest.mark.usefixtures("empty_test_db")
class TestResetPasswordToken:
    def test_reset_password_token(stubbed_encode, app, create_user):
        user = create_user()

        with freeze_time(time.ctime(time.time())):
            ten_minutes = time.time() + 600
            payload = {"user_id": user.id, "exp": ten_minutes}

            with patch.object(jwt, "encode") as stubbed_encode:
                user.reset_password_token()

            stubbed_encode.assert_called_once_with(
                payload, app.secret_key, algorithm="HS256"
            )


def test_full_name(empty_test_db, create_admin_user):
    admin = create_admin_user(firstName="first", lastName="last")
    assert admin.full_name() == "first last"


@pytest.mark.usefixtures("empty_test_db")
class TestFixtures:
    def test_create_admin_user(self, create_admin_user):
        admin = create_admin_user()
        assert admin
        assert admin.type == "admin"

        def test_multiple_admins_can_be_created():
            return create_admin_user()

        assert test_multiple_admins_can_be_created()

    def test_create_join_staff(self, create_join_staff):
        staff = create_join_staff()
        assert staff
        assert staff.type == "staff"

        def test_multiple_join_staff_can_be_created():
            return create_join_staff()

        assert test_multiple_join_staff_can_be_created()

    def test_create_property_manager(self, create_property_manager):
        pm = create_property_manager()
        assert pm
        assert pm.type == "property_manager"

        def test_multiple_pms_can_be_created():
            return create_property_manager()

        assert test_multiple_pms_can_be_created()

    def test_create_unauthorized_user(self, create_unauthorized_user):
        user = create_unauthorized_user()
        assert user.type == "user"

        def test_multiple_users_can_be_created():
            return create_unauthorized_user()

        assert test_multiple_users_can_be_created()
