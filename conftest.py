import pytest
import os
from app import create_app
from db import db
from data.seedData import seedData
from models.user import UserModel
from models.emergency_contact import EmergencyContactModel
from models.contact_number import ContactNumberModel
from models.property import PropertyModel
from models.tenant import TenantModel
from models.tickets import TicketModel
from models.notes import NotesModel
from models.revoked_tokens import RevokedTokensModel

newPropertyName = "test1"
newPropertyAddress = "123 NE FLanders St"

# Note: this repo uses the "pytest-flask" plugin which exposes the following fixtures for use in tests:
#   client: an instance of flask's app.test_client - for making requests i.e. client.get('/')


@pytest.fixture
def app():
    app = create_app()
    return app

@pytest.fixture
def admin_user():
    adminUser = UserModel(email="user4@dwellingly.org", password="1234", firstName="user4", lastName="admin", role="admin", archived=0)
    return adminUser

@pytest.fixture
def new_user():
    newUser = UserModel(email="someone@domain.com", password="1234", firstName="user2", lastName="tester", role="", archived=0)
    return newUser

@pytest.fixture
def property_manager_user():
    return UserModel(email="manager@domain.com", password="1234", firstName="Leslie", lastName="Knope", role="property_manager", archived=0)

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
def new_property():
    newProperty = PropertyModel( name=newPropertyName
                               , address=newPropertyAddress
                               , city="Portland"
                               , state="OR"
                               , zipcode="97207"
                               , propertyManager=5
                               , tenants=3
                               , dateAdded="2020-04-12"
                               , archived=0
                               )
    return newProperty

@pytest.fixture
def empty_database():
    if(os.path.isfile("./data.db")):
        os.remove("./data.db")

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


# -------------     NON-FIXTURE FUNCTIONS     --------------------

# Logs a user in and returns their auth header
# To log a user in, you must also load the "test_database" fixture
def get_auth_header(client, userModel):
    login_response = client.post("/api/login", json={
        "email": userModel.email,
        "password": userModel.password
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
    