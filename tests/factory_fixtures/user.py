import pytest
from models.user import UserModel, RoleEnum

@pytest.fixture
def property_manager_attributes():
    def _property_manager_attributes():
        return {
            "email": "manager@domain.com",
            "password": b'asdf',
            "firstName": "Leslie",
            "lastName": "Knope",
            "phone": "505-503-4455",
            "role": RoleEnum.PROPERTY_MANAGER,
            "archived": False
        }
    yield _property_manager_attributes


@pytest.fixture
def create_property_manager(property_manager_attributes):
    def _create_property_manager():
        pm = UserModel(**property_manager_attributes())
        pm.save_to_db()
        return pm
    yield _create_property_manager
