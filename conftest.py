import pytest
import jwt
from flask import current_app
from app import create_app
from db import db
from data.seedData import seedData
from models.user import UserModel, RoleEnum

from tests.factory_fixtures import *  # noqa: F401, F403

plaintext_password = "1234"


@pytest.fixture
def app():
    app = create_app("testing")
    return app


@pytest.fixture
def admin_user():
    adminUser = UserModel(
        email="user4@dwellingly.org",
        password=plaintext_password,
        firstName="user4",
        lastName="admin",
        phone="555-867-5309",
        role=RoleEnum.ADMIN,
        archived=0,
    )
    return adminUser


@pytest.fixture
def new_user():
    newUser = UserModel(
        email="someone@domain.com",
        password=plaintext_password,
        firstName="user2",
        lastName="tester",
        phone="1-888-cal-saul",
        archived=0,
    )
    return newUser


@pytest.fixture
def valid_header(admin_header):
    return admin_header


def _user_claims(user):
    return {
        "sub": user.id,
        "email": user.email,
        "phone": user.phone,
        "firstName": user.firstName,
        "lastName": user.lastName,
        "role": user.role.value,
    }


@pytest.fixture
def header():
    def _header(user):
        token = jwt.encode(
            _user_claims(user),
            current_app.secret_key,
            algorithm="HS256",
        )
        return {"Authorization": f"Bearer {token}"}

    yield _header


@pytest.fixture
def admin_header(header, create_admin_user):
    return header(create_admin_user())


@pytest.fixture
def staff_header(header, create_join_staff):
    def _staff_header(staff=None):
        return header(staff or create_join_staff())

    yield _staff_header


@pytest.fixture
def pm_header(header, create_property_manager):
    def _pm_header(pm=None):
        return header(pm or create_property_manager())

    yield _pm_header


@pytest.fixture
def test_database(app, admin_user, new_user):
    db.create_all()

    seedData()

    db.session.add(admin_user)
    db.session.add(new_user)
    db.session.commit()

    yield db
    db.drop_all()


@pytest.fixture
def empty_test_db(app):
    db.create_all()

    yield

    db.drop_all()


# -------------     NON-FIXTURE FUNCTIONS     --------------------
def has_valid_headers(response):
    if response.content_type != "application/json":
        return False
    elif "*" not in response.access_control_allow_origin:
        return False
    return True


def is_valid(response, expected_status_code):
    if not has_valid_headers(response):
        return False
    if response.status_code != expected_status_code:
        return False
    return True


# A debug function that prints useful response data
# Be sure to run "pytest -s" to allow console prints
def log(response):
    print(f"\n\nResponse Status: {response.status}")
    print(f"Response JSON: {response.json}")
    print(f"Response headers:\n\n{response.headers}")
