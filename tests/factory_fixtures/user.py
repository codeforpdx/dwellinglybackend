import pytest
from models.user import UserModel, RoleEnum

@pytest.fixture
def create_property_manager():
    def _create_property_manager():
        pm = UserModel(
                email="manager@domain.com",
                password="asdf",
                firstName="Leslie",
                lastName="Knope",
                phone="505-503-4455",
                role=RoleEnum.PROPERTY_MANAGER,
                archived=False
            )
        pm.save_to_db()
        return pm
    yield _create_property_manager


@pytest.fixture
def create_admin_user():
    def _create_admin_user(firstName="Dwellingly", lastName="Admin"):
        admin = UserModel(
                email="admin@dwellingly.com",
                password="asdf",
                firstName=firstName,
                lastName=lastName,
                phone="505-503-1111",
                role=RoleEnum.ADMIN,
                archived=False
            )
        admin.save_to_db()
        return admin
    yield _create_admin_user
