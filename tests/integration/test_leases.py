import pytest
from freezegun import freeze_time
from conftest import is_valid
from models.user import UserModel, RoleEnum
from models.property import PropertyModel
from models.lease import LeaseModel
from models.tenant import TenantModel
from tests.time import Time
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


@pytest.mark.usefixtures('client_class', 'empty_test_db')
class TestGetLease:
    def setup(self):
        self.endpoint = '/api/lease'

    def test_authorized_request_for_a_lease(self, valid_header, create_lease):
        lease = create_lease()

        response = self.client.get(
                f'{self.endpoint}/{lease.id}',
                headers=valid_header
            )

        assert is_valid(response, 200)
        assert response.json == lease.json()

    def test_authorized_request_for_a_non_existent_lease(self, valid_header):
        response = self.client.get(
                f'{self.endpoint}/504',
                headers=valid_header
            )

        assert is_valid(response, 404)
        assert response.json == {'message': 'Lease not found'}

    def test_unauthorized_request_for_a_lease(self):
        response = self.client.get(f'{self.endpoint}/1')

        assert is_valid(response, 401)
        assert response.json == {'message': 'Missing authorization header'}

    def test_authorized_request_for_all_leases(self, valid_header, create_lease):
        lease = create_lease()
        another_lease = create_lease(name='World')

        response = self.client.get(self.endpoint, headers=valid_header)

        assert is_valid(response, 200)
        assert response.json == {
                "Leases": [
                    lease.json(),
                    another_lease.json()
                ]
            }

    def test_unauthorized_request_for_all_leases(self):
        response = self.client.get(self.endpoint)

        assert is_valid(response, 401)
        assert response.json == {'message': 'Missing authorization header'}


@pytest.mark.usefixtures('client_class', 'empty_test_db')
class TestCreateLease:
    def setup(self):
        self.endpoint = '/api/lease'

        self.valid_payload = {
                'dateTimeStart': Time.today(),
                'dateTimeEnd': Time.one_year_from_now(),
                'tenantID': 1
            }
        self.invalid_payload = {}

    def test_authorized_request_with_valid_payload(self, valid_header):
        response = self.client.post(self.endpoint, json=self.valid_payload, headers=valid_header)


        assert is_valid(response, 201)
        assert response.json == {'message': 'Lease created successfully'}
        assert len(LeaseModel.query.all()) == 1

    def test_unauthorized_request_with_valid_payload(self):
        response = self.client.post(self.endpoint, json=self.valid_payload)

        assert is_valid(response, 401)
        assert response.json == {'message': 'Missing authorization header'}

    def test_authorized_request_with_invalid_payload(self, valid_header):
        with pytest.raises(TypeError):
            response = self.client.post(self.endpoint, json=self.invalid_payload, headers=valid_header)


@pytest.mark.usefixtures('client_class', 'empty_test_db')
class TestDeleteLease:
    def setup(self):
        self.endpoint = '/api/lease'

    def test_authorized_request_with_valid_lease_id(self, valid_header, create_lease):
        lease = create_lease()

        response = self.client.delete(f'{self.endpoint}/{lease.id}', headers=valid_header)

        assert is_valid(response, 200)
        assert response.json == {'message': 'Lease removed from database'}
        assert len(LeaseModel.query.all()) == 0

    def test_authorized_request_with_invalid_lease_id(self, valid_header):
        response = self.client.delete(f'{self.endpoint}/504', headers=valid_header)

        assert is_valid(response, 404)
        assert response.json == {'message': 'Lease not found'}


@pytest.mark.usefixtures('client_class', 'empty_test_db')
class TestUpdateLease:
    def setup(self):
        self.endpoint = '/api/lease'

    def test_invalid_lease_id(self, valid_header):
        response = self.client.put(f'{self.endpoint}/504', headers=valid_header)

        assert is_valid(response, 404)
        assert response.json == {'message': 'Lease not found'}

    def test_date_is_updated_with_valid_payload(self, valid_header, create_lease):
        lease = create_lease()

        payload = {'dateTimeEnd': Time.one_year_from_now()}
        old_date = Time.format_date(lease.dateUpdated)

        with freeze_time(Time.one_year_from_now()):
            response = self.client.put(f'{self.endpoint}/{lease.id}', json=payload, headers=valid_header)

            assert is_valid(response, 200)
            assert response.json['dateUpdated'] != old_date

    def test_updatedDate_is_left_unchanged_when_given_invalid_params(self, valid_header, create_lease):
        lease = create_lease()
        old_date = Time.format_date(lease.dateUpdated)

        with freeze_time(Time.one_year_from_now()):
            response = self.client.put(f'{self.endpoint}/{lease.id}', json={}, headers=valid_header)

        assert is_valid(response, 400)
        assert response.json['dateUpdated'] == old_date

    def test_invalid_attribute_ids(self, valid_header, create_lease):
        lease = create_lease('Hello')

        payload = {
                'name': 'I',
                'landlordID': '504',
                'propertyID': '504',
                'tenantID': '504',
                'occupants': '504',
                'dateTimeStart': Time.one_year_from_now(),
                'dateTimeEnd': Time.today()
            }

        with pytest.raises(AttributeError):
            response = self.client.put(f'{self.endpoint}/{lease.id}', json=payload, headers=valid_header)

    def test_valid_attrs_are_all_updated(self, valid_header, create_lease, create_tenant, create_property, create_landlord):
        lease = create_lease()
        new_landlord = create_landlord()
        new_tenant = create_tenant()
        new_property = create_property(new_landlord)
        start_date = Time.one_year_from_now()
        end_date = Time.today()

        payload = {
                'name': 'I',
                'landlordID': new_landlord.id,
                'propertyID': new_property.id,
                'tenantID': new_tenant.id,
                'occupants': '200',
                'dateTimeStart': start_date,
                'dateTimeEnd': end_date
            }

        response = self.client.put(f'{self.endpoint}/{lease.id}', json=payload, headers=valid_header)

        assert is_valid(response, 200)
        assert response.json['name'] == 'I'
        assert response.json['landlordID']['id'] == new_landlord.id
        assert response.json['propertyID']['id'] == new_property.id
        assert response.json['tenantID']['id'] == new_tenant.id
        assert response.json['occupants'] == 200
        assert response.json['dateTimeStart'] == start_date
        assert response.json['dateTimeEnd'] == end_date
        assert response.json == lease.json()


@pytest.mark.usefixtures('client_class', 'empty_test_db')
class TestLeaseAuthorizations:
    def setup(self):
        self.valid_payload = {
                'dateTimeStart': Time.today(),
                'dateTimeEnd': Time.one_year_from_now(),
                'tenantID': 1
            }
    # Test auth is in place at each endpoint
    def test_unauthorized_get_request(self):
        response = self.client.get('/api/lease/1')

        assert is_valid(response, 401)
        assert response.json == {'message': 'Missing authorization header'}

    def test_unauthorized_get_all_request(self):
        response = self.client.get('/api/lease')

        assert is_valid(response, 401)
        assert response.json == {'message': 'Missing authorization header'}

    def test_unauthorized_create_request(self):
        response = self.client.post('/api/lease')

        assert is_valid(response, 401)
        assert response.json == {'message': 'Missing authorization header'}

    def test_unauthorized_delete_request(self):
        response = self.client.delete('/api/lease/1')

        assert is_valid(response, 401)
        assert response.json == {'message': 'Missing authorization header'}

    def test_unauthorized_update_request(self):
        response = self.client.put('/api/lease/1')

        assert is_valid(response, 401)
        assert response.json == {'message': 'Missing authorization header'}

    # Test all roles are authorized to access each endpoint
    def test_pm_authorized_to_get(self, pm_header, create_lease):
        lease = create_lease()

        response = self.client.get(f'/api/lease/{lease.id}', headers=pm_header)
        assert is_valid(response, 200)

    def test_staff_are_authorized_to_get(self, staff_header, create_lease):
        lease = create_lease()

        response = self.client.get(f'/api/lease/{lease.id}', headers=staff_header)
        assert is_valid(response, 200)

    def test_admin_is_authorized_to_get(self, admin_header, create_lease):
        lease = create_lease()

        response = self.client.get(f'/api/lease/{lease.id}', headers=admin_header)
        assert is_valid(response, 200)

    def test_pm_is_authorized_to_get_all(self, pm_header, create_lease):
        lease = create_lease()

        response = self.client.get('/api/lease', headers=pm_header)
        assert is_valid(response, 200)

    def test_staff_are_authorized_to_get_all(self, staff_header, create_lease):
        lease = create_lease()

        response = self.client.get('/api/lease', headers=staff_header)
        assert is_valid(response, 200)

    def test_admin_is_authorized_to_get_all(self, admin_header, create_lease):
        lease = create_lease()

        response = self.client.get('/api/lease', headers=admin_header)
        assert is_valid(response, 200)

    def test_pm_is_authorized_to_create(self, pm_header):
        response = self.client.post('/api/lease', json=self.valid_payload, headers=pm_header)

        assert is_valid(response, 201)

    def test_staff_are_authorized_to_create(self, staff_header):
        response = self.client.post('/api/lease', json=self.valid_payload, headers=staff_header)
        assert is_valid(response, 201)

    def test_admin_is_authorized_to_create(self, admin_header):
        response = self.client.post('/api/lease', json=self.valid_payload, headers=admin_header)
        assert is_valid(response, 201)

    def test_pm_is_authorized_to_delete_lease(self, pm_header, create_lease):
        lease = create_lease()
        response = self.client.delete(f'/api/lease/{lease.id}'.format(id), headers=pm_header)

        assert is_valid(response, 200)

    def test_staff_are_authorized_to_delete_lease(self, staff_header, create_lease):
        lease = create_lease()
        response = self.client.delete(f'/api/lease/{lease.id}'.format(id), headers=staff_header)

        assert is_valid(response, 200)

    def test_admin_is_authorized_to_delete_lease(self, admin_header, create_lease):
        lease = create_lease()
        response = self.client.delete(f'/api/lease/{lease.id}'.format(id), headers=admin_header)

        assert is_valid(response, 200)

    def test_pm_is_authorized_to_update(self, pm_header, create_lease):
        lease = create_lease()
        payload = {
                'dateTimeStart': Time.today(),
                'dateTimeEnd': Time.one_year_from_now()
            }
        response = self.client.put(f'/api/lease/{lease.id}', json=payload, headers=pm_header)
        assert is_valid(response, 200)

    def test_staff_authorized_to_update(self, staff_header, create_lease):
        lease = create_lease()
        payload = {
                'dateTimeStart': Time.today(),
                'dateTimeEnd': Time.one_year_from_now()
            }
        response = self.client.put(f'/api/lease/{lease.id}', json=payload, headers=staff_header)
        assert is_valid(response, 200)

    def test_admin_authorized_to_update(self, admin_header, create_lease):
        lease = create_lease()
        payload = {
                'dateTimeStart': Time.today(),
                'dateTimeEnd': Time.one_year_from_now()
            }
        response = self.client.put(f'/api/lease/{lease.id}', json=payload, headers=admin_header)
        assert is_valid(response, 200)
