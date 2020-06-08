import pytest
from app import create_app
from models.user import UserModel

@pytest.fixture
def app():
    app = create_app()
    return app

@pytest.fixture(scope="module")
def new_user():
    user = UserModel(email="user1@dwellingly.org", role="admin", firstName="user1", lastName="tester", password="1234", archived=0)
    return user