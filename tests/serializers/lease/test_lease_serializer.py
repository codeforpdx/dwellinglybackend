import pytest
import json
from models.user import UserModel, RoleEnum
from models.property import PropertyModel
from models.lease import LeaseModel
from models.tenant import TenantModel
from datetime import datetime
from tests.time import Time
from serializers.lease import LeaseSerializer

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
def create_property():
    def _create_property(pm):
        property = PropertyModel(
                name='the heights',
                address='111 SW Harrison',
                city="Portland",
                unit="101",
                state="OR",
                zipcode="97207",
                propertyManager=pm.id,
                dateAdded="2020-04-12",
                archived=False
            )
        property.save_to_db()
        return property
    yield _create_property

@pytest.fixture
def create_landlord():
    def _create_landlord():
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
    yield _create_landlord

def lease_attributes(name, tenant, landlord, property):
    return {
        "name": name,
        "tenantID": tenant.id,
        "landlordID": landlord.id,
        "propertyID": property.id,
        "dateTimeStart": datetime.now(),
        "dateTimeEnd": datetime.now(),
        "dateUpdated": datetime.now(),
        "occupants": 3
    }

@pytest.fixture
def create_lease(create_landlord, create_property, create_tenant):
    def _create_lease(name="Hello World", tenant=create_tenant(), landlord=create_landlord(), property=None):
        if not property:
            property = create_property(landlord)
        lease = LeaseModel(**lease_attributes(name, tenant, landlord, property))
        lease.save_to_db()
        return lease
    yield _create_lease


@pytest.mark.usefixtures('empty_test_db')
class TestLeaseSerializer:
    def setup(self):
        pass

    def test_serializer(self, create_lease):
        lease = create_lease()
        property = LeaseModel.find_by_id(lease.propertyID)
        landlord = UserModel.find_by_id(lease.landlordID)

        assert LeaseSerializer.serialize(lease) == {
                'id': lease.id,
                'name': lease.name,
                'dateTimeStart': Time.format_date(lease.dateTimeStart),
                'dateTimeEnd': Time.format_date(lease.dateTimeEnd),
                'dateUpdated': Time.format_date(lease.dateUpdated),
                'occupants': lease.occupants,
                'created_at': Time.format_date(lease.created_at),
                'updated_at': lease.updated_at
            }
