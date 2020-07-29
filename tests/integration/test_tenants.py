from conftest import is_valid, log

# NOTE: Each endpoint should be tested for all valid request types (GET, POST, PUT, PATCH, DELETE, etc.)

  # Each request should be tested to return valid:
    # 1. Status Code
    # 2. Headers
    # 3. JSON

  # Also test invalid requests, such as:
    # 1. Action on non-existent entries
    # 2. Duplicate creation

  # Also test for appropriate auth restriction, such as:
    # 1. Valid access token
    # 2. Valid role (admin, property-manager, pending, etc.)

endpoint = '/api/tenants'

def test_tenants_GET_all(client, test_database, auth_headers):
  response = client.get(endpoint, headers=auth_headers["admin"])
  assert is_valid(response, 200) # OK
  assert response.json['tenants'][0]['firstName'] == 'Renty'


def test_tenants_GET_one(client, test_database, auth_headers):
  id = 1
  response = client.get(f'{endpoint}/{id}', headers=auth_headers["admin"])
  assert is_valid(response, 200) # OK
  assert response.json['firstName'] == 'Renty'
  
  id = 100
  response = client.get(f'{endpoint}/{id}', headers=auth_headers["admin"])
  assert is_valid(response, 404) # NOT FOUND - 'Tenant not found'


def test_tenants_POST(client, auth_headers):
  newTenant = {
    "firstName": "Jake", 
    "lastName": "The Dog",
    "phone": "111-111-1111",
    "propertyID": 1,
    "staffIDs": [1, 2] 
  }

  response = client.post(endpoint, json=newTenant, headers=auth_headers["admin"])
  assert is_valid(response, 201) # CREATED
  assert response.json['firstName'] == 'Jake'

  response = client.post(endpoint, json=newTenant, headers=auth_headers["admin"])
  assert is_valid(response, 401) # UNAUTHORIZED - A tenant with this first and last name already exists

  response = client.post(endpoint, json=newTenant, headers=auth_headers["pm"])
  assert is_valid(response, 401) # UNAUTHORIZED - Admin Access Required

  response = client.post(endpoint, json=newTenant, headers=auth_headers["pending"]) 
  assert is_valid(response, 401) # UNAUTHORIZED - Admin Access Required

  response = client.post(endpoint, json=newTenant)
  assert is_valid(response, 401) # UNAUTHORIZED - Missing Authorization Header

  newTenant = {}
  response = client.post(endpoint, json=newTenant, headers=auth_headers["admin"])
  assert is_valid(response, 400) # BAD REQUEST - {'firstName': 'This field cannot be blank.'}


def test_tenants_PUT(client, auth_headers):
  id = 1
  updatedTenant = {
    "firstName": "Jake", 
    "lastName": "The Dog",
    "phone": "111-111-1111",
    "propertyID": 1,
    "staffIDs": [1, 2] 
  }
  response = client.put(f'{endpoint}/{id}', json=updatedTenant, headers=auth_headers["admin"])
  assert is_valid(response, 200) # OK
  assert response.json['firstName'] == 'Jake'

  id = 100
  response = client.put(f'{endpoint}/{id}', json=updatedTenant, headers=auth_headers["admin"])
  assert is_valid(response, 404) # NOT FOUND


def test_tenants_DELETE(client, auth_headers):
  id = 1

  response = client.delete(f'{endpoint}/{id}')
  assert is_valid(response, 401) # UNAUTHORIZED - Missing Authorization Header

  response = client.delete(f'{endpoint}/{id}', headers=auth_headers["pending"])
  assert is_valid(response, 401) # UNAUTHORIZED - Admin Access Required

  response = client.delete(f'{endpoint}/{id}', headers=auth_headers["pm"])
  assert is_valid(response, 401) # UNAUTHORIZED - Admin Access Required

  response = client.delete(f'{endpoint}/{id}', headers=auth_headers["admin"])
  assert is_valid(response, 200) # OK

  response = client.delete(f'{endpoint}/{id}', headers=auth_headers["admin"])
  assert is_valid(response, 404) # NOT FOUND - Emergency Contact not found