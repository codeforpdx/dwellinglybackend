import pytest
import random
from models.user import UserModel, RoleEnum
from models.users.admin import Admin
from models.users.staff import Staff
from models.users.property_manager import PropertyManager


@pytest.fixture
def user_attributes(faker):
    def _user_attributes(
        role=None, archived=False, firstName=None, lastName=None, pw=None
    ):
        attrs = {
            "email": faker.unique.email(),
            "password": pw if pw else faker.password(),
            "firstName": firstName if firstName else faker.first_name(),
            "lastName": lastName if lastName else faker.last_name(),
            "phone": faker.phone_number(),
            "archived": archived,
        }
        if role:
            return {**attrs, "role": role}
        else:
            return attrs

    yield _user_attributes


@pytest.fixture
def create_admin_user(user_attributes):
    def _create_admin_user(firstName=None, lastName=None, pw=None):
        admin = Admin(
            **user_attributes(
                role=RoleEnum.ADMIN,
                firstName=firstName,
                lastName=lastName,
                pw=pw,
            )
        )
        admin.save_to_db()
        return admin

    yield _create_admin_user


@pytest.fixture
def create_join_staff(user_attributes):
    def _create_join_staff(pw=None):
        staff = Staff(**user_attributes(role=RoleEnum.STAFF, pw=pw))
        staff.save_to_db()
        return staff

    yield _create_join_staff


@pytest.fixture
def create_property_manager(user_attributes):
    def _create_property_manager(pw=None):
        pm = PropertyManager(**user_attributes(role=RoleEnum.PROPERTY_MANAGER, pw=pw))
        pm.save_to_db()
        return pm

    yield _create_property_manager


@pytest.fixture
def create_unauthorized_user(user_attributes):
    def _create_unauthorized_user(pw=None):
        user = UserModel(**user_attributes(pw=pw))
        user.save_to_db()
        return user

    yield _create_unauthorized_user


@pytest.fixture
def create_user(
    user_attributes, create_admin_user, create_join_staff, create_property_manager
):
    def _create_user(pw=None, admin=True):
        if admin:
            return random.choice(
                [
                    create_admin_user(pw=pw),
                    create_join_staff(pw=pw),
                    create_property_manager(pw=pw),
                ]
            )
        else:
            return random.choice(
                [create_join_staff(pw=pw), create_property_manager(pw=pw)]
            )

    yield _create_user
