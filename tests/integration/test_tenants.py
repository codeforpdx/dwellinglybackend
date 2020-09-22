from conftest import is_valid, log

endpoint = '/api/tenants'


def test_tenants_GET_all(client, test_database, auth_headers):
    response = client.get(endpoint, headers=auth_headers["admin"])
    assert is_valid(response, 200)  # OK
    assert response.json['tenants'][0]['firstName'] == 'Renty'


def test_tenants_GET_one(client, test_database, auth_headers):
    id = 1
    response = client.get(f'{endpoint}/{id}', headers=auth_headers["admin"])
    assert is_valid(response, 200)  # OK
    assert response.json['firstName'] == 'Renty'

    id = 100
    response = client.get(f'{endpoint}/{id}', headers=auth_headers["admin"])
    assert is_valid(response, 404)  # NOT FOUND - 'Tenant not found'


def test_tenants_POST(client, auth_headers):
    newTenant = {
        "firstName": "Jake",
        "lastName": "The Dog",
        "phone": "111-111-1111",
        "propertyID": 1,
        "staffIDs": [1, 2],
        "unitNum": "237"
    }

    response = client.post(endpoint, json=newTenant,
                           headers=auth_headers["admin"])
    assert is_valid(response, 201)  # CREATED
    assert response.json['firstName'] == 'Jake'

    response = client.post(endpoint, json=newTenant,
                           headers=auth_headers["admin"])
    # UNAUTHORIZED - A tenant with this first and last name already exists
    assert is_valid(response, 401)

    response = client.post(endpoint, json=newTenant,
                           headers=auth_headers["pm"])
    assert is_valid(response, 401)  # UNAUTHORIZED - Admin Access Required

    response = client.post(endpoint, json=newTenant,
                           headers=auth_headers["pending"])
    assert is_valid(response, 401)  # UNAUTHORIZED - Admin Access Required

    response = client.post(endpoint, json=newTenant)
    # UNAUTHORIZED - Missing Authorization Header
    assert is_valid(response, 401)

    newTenant = {}
    response = client.post(endpoint, json=newTenant,
                           headers=auth_headers["admin"])
    # BAD REQUEST - {'firstName': 'This field cannot be blank.'}
    assert is_valid(response, 400)


def test_tenants_PUT(client, auth_headers):
    id = 1
    updatedTenant = {
        "firstName": "Jake",
        "lastName": "The Dog",
        "phone": "111-111-1111",
        "propertyID": 1,
        "staffIDs": [1, 2],
        "unitNum": "237"
    }
    response = client.put(f'{endpoint}/{id}',
                          json=updatedTenant, headers=auth_headers["admin"])
    assert is_valid(response, 200)  # OK
    assert response.json['firstName'] == 'Jake'

    id = 100
    response = client.put(f'{endpoint}/{id}',
                          json=updatedTenant, headers=auth_headers["admin"])
    assert is_valid(response, 404)  # NOT FOUND


def test_unauthenticated_delete(client):
    response = client.delete(f'{endpoint}/1')

    assert is_valid(response, 401)

def test_pending_role_is_unauthorized_to_delete(client, auth_headers):
    response = client.delete(
        f'{endpoint}/1', headers=auth_headers["pending"])

    assert is_valid(response, 401)

def test_pm_role_is_unauthorized_to_delete(client, auth_headers):
    response = client.delete(f'{endpoint}/1', headers=auth_headers["pm"])

    assert is_valid(response, 401)

def test_admin_is_authorized_to_delete(client, auth_headers):
    response = client.delete(f'{endpoint}/1', headers=auth_headers["admin"])
    assert is_valid(response, 200)

def test_resource_not_found(client, auth_headers):
    response = client.delete(f'{endpoint}/10000', headers=auth_headers["admin"])
    assert is_valid(response, 404)
