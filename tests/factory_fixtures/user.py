import pytest
from models.user import UserModel, RoleEnum

@pytest.fixture
def user_attributes(faker):
    def _user_attributes(role=None, archived=False, firstName=None, lastName=None):
        return {
            "email": faker.unique.email(),
            "password": faker.password(),
            "firstName": firstName if firstName else faker.first_name(),
            "lastName": lastName if lastName else faker.last_name(),
            "phone": faker.phone_number(),
            "role": role,
            "archived": archived
        }
    yield _user_attributes

@pytest.fixture
def create_admin_user(user_attributes):
    def _create_admin_user(firstName=None, lastName=None):
        admin = UserModel(**user_attributes(
            role=RoleEnum.ADMIN,
            firstName=firstName,
            lastName=lastName)
        )
        admin.save_to_db()
        return admin

    yield _create_admin_user

@pytest.fixture
def create_join_staff(user_attributes):
    def _create_join_staff():
        staff = UserModel(**user_attributes(role=RoleEnum.STAFF))
        staff.save_to_db()
        return staff

    yield _create_join_staff

@pytest.fixture
def create_property_manager(user_attributes):
    def _create_property_manager():
        pm = UserModel(**user_attributes(role=RoleEnum.PROPERTY_MANAGER))
        pm.save_to_db()
        return pm

    yield _create_property_manager

@pytest.fixture
def create_unauthorized_user(user_attributes):
    def _create_unauthorized_user():
        user = UserModel(**user_attributes())
        user.save_to_db()
        return user

    yield _create_unauthorized_user
