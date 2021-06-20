import pytest
from models.user import UserModel, RoleEnum
from schemas.user import UserSchema
from unittest.mock import patch
import jwt
import time
from freezegun import freeze_time


@patch.object(jwt, "encode")
def test_reset_password_token(stubbed_encode, app, test_database):
    user = UserModel.find(1)

    with freeze_time(time.ctime(time.time())):
        ten_minutes = time.time() + 600
        payload = {"user_id": user.id, "exp": ten_minutes}

        assert user.reset_password_token()
        stubbed_encode.assert_called_once_with(
            payload, app.secret_key, algorithm="HS256"
        )


def test_full_name(empty_test_db, create_admin_user):
    admin = create_admin_user(firstName="first", lastName="last")
    assert admin.full_name() == "first last"


@pytest.mark.usefixtures("empty_test_db")
class TestFindUsersWithoutAssignedRole:
    def test_find_users_authorized_active(self, create_admin_user):
        _ = create_admin_user()

        found_user = UserModel.find_users_without_assigned_role()
        assert found_user.first() is None

    def test_find_users_authorized_inactive(self, create_admin_user):
        user = create_admin_user()
        user.archived = True
        user.save_to_db()

        found_user = UserModel.find_users_without_assigned_role()
        assert found_user.first() is None

    def test_find_users_unauthorized_active(self, create_unauthorized_user):
        user = create_unauthorized_user()

        found_user = UserModel.find_users_without_assigned_role()
        assert found_user.first() == user

    def test_find_users_unauthorized_inactive(self, create_unauthorized_user):
        user = create_unauthorized_user()
        user.archived = True
        user.save_to_db()

        found_user = UserModel.find_users_without_assigned_role()
        assert found_user.first() is None


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
        assert user.role is None

        def test_multiple_users_can_be_created():
            return create_unauthorized_user()

        assert test_multiple_users_can_be_created()


@pytest.mark.usefixtures("empty_test_db")
class TestOverwrittenAndInheritedMethods:
    def test_user_save_to_db(self, user_attributes):
        attrs = UserModel.validate(
            UserSchema, user_attributes(role=RoleEnum.STAFF.value)
        )
        user = UserModel(**attrs)
        user.save_to_db()
        lookedup = UserModel.find(user.id)
        assert lookedup.password is None

    def test_update_class_method(self, create_join_staff, faker):
        user = create_join_staff()
        email = faker.unique.email()
        UserModel.update(UserSchema, user.id, {"email": email})
        lookedup = UserModel.find(user.id)
        assert lookedup.email == email
        assert lookedup.password == user.password

    def test_create_class_method(self, user_attributes):
        user = UserModel.create(UserSchema, user_attributes(role=RoleEnum.STAFF.value))
        lookedup = UserModel.find(user.id)
        assert lookedup.password is None
