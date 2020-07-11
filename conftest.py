import pytest
import os
from app import create_app
from db import db
from data.seedData import seedData
from models.user import UserModel
from models.emergency_contact import EmergencyContactModel
from models.contact_number import ContactNumberModel

adminUserEmail = "user1@dwellingly.org"
adminRole = "admin"
newUserEmail = "someone@domain.com"
userPassword = "1234"

# Note: this repo uses the "pytest-flask" plugin which exposes the following fixtures for use in tests:
#   client: an instance of flask's app.test_client - for making requests i.e. client.get('/')

@pytest.fixture
def app():
    app = create_app()
    return app


# ----------------     TEST USERS    ------------------

@pytest.fixture
def admin_user():
    adminUser = UserModel(email=adminUserEmail, password=userPassword, firstName="user1", lastName="admin", role=adminRole, archived=0)
    return adminUser

@pytest.fixture
def new_user():
    newUser = UserModel(email=newUserEmail, password=userPassword, firstName="user2", lastName="tester", role="", archived=0)
    return newUser

@pytest.fixture
def property_manager_user():
    return UserModel(email="manager@domain.com", password=userPassword, firstName="Leslie", lastName="Knope", role="property_manager", archived=0)

# Logs a user in and returns the response and auth header
# To log a user in, you must also load the "test_database" fixture
def login_user(client, userModel):
    login_response = client.post("/api/login", json={
        "email": userModel.email,
        "password": userModel.password
    })
    auth_header = {"Authorization": f"Bearer {login_response.json['access_token']}"}
    return login_response, auth_header


# ---------------     TEST DATABASES     ----------------

@pytest.fixture
def empty_database():
    if(os.path.isfile("./data.db")):
        os.remove("./data.db")

@pytest.fixture
def test_database(admin_user, new_user, property_manager_user):
    app = create_app()
    db.create_all()

    db.session.add(admin_user)
    db.session.add(new_user)
    db.session.add(property_manager_user)

    db.session.add(EmergencyContactModel(name="Narcotics Anonymous", description="NA Hotline", contact_numbers=[{"number": "503-345-9839"}]))

    db.session.commit()

    yield db
    db.drop_all()


#----------     EMERGENCY CONTACT & CONTACT NUMBERS     -------------------

emergency_contact_name = "Washington Co. Crisis Team"
emergency_contact_description = "Suicide prevention and referrals"
contact_number = "503-291-9111"
contact_numtype = "Call"

@pytest.fixture
def emergency_contact():
    app = create_app()
    with app.app_context():
        emergencyContact = EmergencyContactModel(name=emergency_contact_name, contact_numbers=[{"number": contact_number, "numtype": contact_numtype}], description=emergency_contact_description)
        return emergencyContact