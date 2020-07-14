import pytest
import os
from app import create_app
from db import db
from data.seedData import seedData
from models.user import UserModel

adminUserEmail = "user1@dwellingly.org"
adminRole = "admin"
newUserEmail = "someone@domain.com"
userPassword = "1234"

@pytest.fixture
def app():
    app = create_app()
    return app

@pytest.fixture
def admin_user():
    adminUser = UserModel(email=adminUserEmail, password=userPassword, firstName="user1", lastName="admin", role=adminRole, archived=0)
    return adminUser

@pytest.fixture
def new_user():
    newUser = UserModel(email=newUserEmail, password=userPassword, firstName="user2", lastName="tester", role="", archived=0)
    return newUser

@pytest.fixture
def empty_database():
    if(os.path.isfile("./data.db")):
        os.remove("./data.db")

@pytest.fixture
def users_in_database(admin_user, new_user):
    app = create_app()
    db.create_all()
    admin_user.save_to_db()
    new_user.save_to_db()
    yield db
    db.drop_all()

@pytest.fixture
def seeded_database():
    app = create_app()
    db.create_all()
    seedData()
    yield db
    db.drop_all()

@pytest.fixture
def admin_logged_in(client, users_in_database, admin_user):
    data = {
        "email": admin_user.email,
        "password": admin_user.password
    }
    response = client.post("/api/login", json=data)
    return response

@pytest.fixture
def admin_auth_header(admin_logged_in):
    header = {"Authorization": f"Bearer {admin_logged_in.json['access_token']}"}
    return header
