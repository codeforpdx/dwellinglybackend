import pytest
from models.user import UserModel, RoleEnum

@pytest.fixture
def create_property_manager():
    def _create_property_manager():
        pm = UserModel(
                email="manager@domain.com",
                password=b'asdf',
                firstName="Leslie",
                lastName="Knope",
                phone="505-503-4455",
                role=RoleEnum.PROPERTY_MANAGER,
                archived=False
            )
        pm.save_to_db()
        return pm
    yield _create_property_manager
