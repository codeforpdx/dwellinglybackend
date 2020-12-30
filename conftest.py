import pytest
import os
from flask import current_app
from app import create_app
from db import db
from data.seedData import seedData
from models.user import UserModel, RoleEnum
from models.property import PropertyModel
import jwt
from tests.factory_fixtures import *

plaintext_password = "1234"

# Note: this repo uses the "pytest-flask" plugin which exposes the following fixtures for use in tests:
#   client: an instance of flask's app.test_client - for making requests i.e. client.get('/')

@pytest.fixture
def app():
    app = create_app('testing')
    return app

@pytest.fixture
def admin_user():
    adminUser = UserModel(email="user4@dwellingly.org", password=plaintext_password, firstName="user4", lastName="admin", phone="555-867-5309", role=RoleEnum.ADMIN, archived=0)
    return adminUser

@pytest.fixture
def new_user():
    newUser = UserModel(email="someone@domain.com", password=plaintext_password, firstName="user2", lastName="tester", phone="1-888-cal-saul", role=RoleEnum.PENDING, archived=0)
    return newUser

@pytest.fixture
def property_manager_user():
    return UserModel(email="manager@domain.com", password=plaintext_password, firstName="Leslie", lastName="Knope", phone="505-503-4455", role=RoleEnum.PROPERTY_MANAGER, archived=0)

#Returns an object with authorization headers for users of all roles (admin, property-manager, pending)
@pytest.fixture
def auth_headers(client, test_database, admin_user, new_user, property_manager_user):
    admin_auth_header = get_auth_header(client, admin_user)
    pm_auth_header = get_auth_header(client, property_manager_user)
    pending_auth_header = get_auth_header(client, new_user)

    return {
        "admin": admin_auth_header,
        "pm": pm_auth_header,
        "pending": pending_auth_header
    }

@pytest.fixture
def valid_header(admin_header):
    return admin_header

def _user_claims(user):
    return {
        'email': user.email,
        'phone': user.phone,
        'firstName': user.firstName,
        'lastName': user.lastName,
        'role': user.role.value
    }

@pytest.fixture
def admin_header(create_admin_user):
    admin = create_admin_user()
    token = jwt.encode({
            'identity': admin.id,
            'user_claims': _user_claims(admin)
        },
            current_app.secret_key,algorithm='HS256'
        ).decode('utf-8')
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture
def staff_header(create_join_staff):
    staff = create_join_staff()
    token = jwt.encode({
            'identity': staff.id,
            'user_claims': _user_claims(staff)
        },
            current_app.secret_key,algorithm='HS256'
        ).decode('utf-8')
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture
def pm_header(create_property_manager):
    pm = create_property_manager()
    token = jwt.encode({
            'identity': pm.id,
            'user_claims': _user_claims(pm)        },
            current_app.secret_key,algorithm='HS256'
        ).decode('utf-8')
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture
def test_database(app, admin_user, new_user, property_manager_user):
    db.create_all()

    seedData()

    db.session.add(admin_user)
    db.session.add(new_user)
    db.session.add(property_manager_user)
    db.session.commit()

    yield db
    db.drop_all()


@pytest.fixture
def empty_test_db(app):
    db.create_all()

    yield

    db.drop_all()

# -------------     NON-FIXTURE FUNCTIONS     --------------------

# Logs a user in and returns their auth header
# To log a user in, you must also load the "test_database" fixture
def get_auth_header(client, userModel):
    login_response = client.post("/api/login", json={
        "email": userModel.email,
        "password": plaintext_password
    })
    auth_header = {"Authorization": f"Bearer {login_response.json['access_token']}"}
    return auth_header

def has_valid_headers(response):
    if (response.content_type != "application/json"):
        return False
    elif ("*" not in response.access_control_allow_origin):
        return False
    return True

def is_valid(response, expected_status_code):
    if (not has_valid_headers(response)):
        return False
    if (response.status_code != expected_status_code):
        return False
    return True

# A debug function that prints useful response data
# Be sure to run "pytest -s" to allow console prints
def log(response):
    print(f'\n\nResponse Status: {response.status}')
    print(f'Response JSON: {response.json}')
    print(f'Response headers:\n\n{response.headers}')
