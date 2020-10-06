import pytest
from models.user import UserModel, RoleEnum
from models.property import PropertyModel
from models.lease import LeaseModel
from models.tenant import TenantModel
from datetime import datetime

@pytest.fixture
def create_tenant():
    def _create_tenant():
        tenant = TenantModel(
                firstName="firstName",
                lastName="lastName",
                phone="phone",
                propertyID=None,
                staffIDs=[],
                unitNum=3
            )
        tenant.save_to_db()
        return tenant
    yield _create_tenant

@pytest.fixture
def create_property_manager():
    def _create_property_manager():
        landlord = UserModel(
                email="manager@domain.com",
                password=b'asdf',
                firstName="Leslie",
                lastName="Knope",
                phone="505-503-4455",
                role=RoleEnum.PROPERTY_MANAGER,
                archived=False
            )
        landlord.save_to_db()
        return landlord
    yield _create_property_manager

@pytest.fixture
def create_property(create_property_manager):
    def _create_property():
        property = PropertyModel(
                name='the heights',
                address='111 SW Harrison',
                city="Portland",
                unit="101",
                state="OR",
                zipcode="97207",
                propertyManager=create_property_manager().id,
                dateAdded="2020-04-12",
                archived=False
            )
        property.save_to_db()
        return property
    yield _create_property

def lease_attributes(name, tenant, property):
    return {
        "name": name,
        "tenantID": tenant.id,
        "propertyID": property.id,
        "dateTimeStart": datetime.now(),
        "dateTimeEnd": datetime.now(),
        "dateUpdated": datetime.now(),
        "occupants": 3
    }

@pytest.fixture
def create_lease(create_property, create_tenant):
    def _create_lease(name="Hello World", tenant=create_tenant(), property=create_property()):
        lease = LeaseModel(**lease_attributes(name, tenant, property))
        lease.save_to_db()
        return lease
    yield _create_lease
