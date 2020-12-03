import pytest
from models.user import UserModel, RoleEnum

@pytest.fixture
<<<<<<< HEAD
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
=======
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

@pytest.fixture
def create_join_staff():
    def _create_join_staff():
        staff = UserModel(
                email="staffer@example.com",
                password="asdf",
                firstName="File",
                lastName="Last",
                phone="503-555-hello",
                role=RoleEnum.STAFF,
                archived=False
            )
        staff.save_to_db()
        return staff
    yield _create_join_staff

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
>>>>>>> development
        pm.save_to_db()
        return pm
    yield _create_property_manager
