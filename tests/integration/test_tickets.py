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

endpoint = '/api/tickets'

def test_tickets_GET_all(client, auth_headers):
  response = client.get(endpoint, headers=auth_headers["admin"])
  assert is_valid(response, 200) # OK
  assert response.json['Tickets'][0]['issue'] == 'The roof, the roof, the roof is one fire.'


def test_tickets_GET_one(client, auth_headers):
  id = 1
  response = client.get(f'{endpoint}/{id}', headers=auth_headers["admin"])
  assert is_valid(response, 200) # OK
  assert response.json['issue'] == 'The roof, the roof, the roof is one fire.'
  
  id = 100
  response = client.get(f'{endpoint}/{id}', headers=auth_headers["admin"])
  assert is_valid(response, 404) # NOT FOUND - 'Tenant not found'


def test_tickets_POST(client, auth_headers):
  newTicket = {
    "issue": "The roof, the roof, the roof is one fire.",
    "tenant": 1,
    "sender": 1, 
    "status": "In Progress",
    "urgency": "Low",
    "assignedUser": 1
  }

  response = client.post(endpoint, json=newTicket, headers=auth_headers["admin"])
  assert is_valid(response, 201) # CREATED
  assert response.json['issue'] == 'The roof, the roof, the roof is one fire.'

  response = client.post(endpoint, json=newTicket)
  assert is_valid(response, 401) # UNAUTHORIZED - Missing Authorization Header

  # TODO: An empty ticket crashes the server.
  # newTicket = {}
  # response = client.post(endpoint, json=newTicket, headers=auth_headers["admin"])
  # log(response)
  # assert is_valid(response, 400) # BAD REQUEST - {'firstName': 'This field cannot be blank.'}


def test_tickets_PUT(client, auth_headers):
  id = 1
  updatedTicket = {
    "issue": "The roof, the roof, the roof is one fire.",
    "tenant": 1,
    "sender": 1, 
    "status": "In Progress",
    "urgency": "Low",
    "assignedUser": 1
  }
  response = client.put(f'{endpoint}/{id}', json=updatedTicket, headers=auth_headers["admin"])
  assert is_valid(response, 200) # OK
  assert response.json['issue'] == 'The roof, the roof, the roof is one fire.'

  # TODO: A request to put a non-existant ticket should return a 400 status
  # id = 100
  # response = client.put(f'{endpoint}/{id}', json=updatedTicket, headers=auth_headers["admin"])
  # log(response)
  # assert is_valid(response, 404) # NOT FOUND


def test_tickets_DELETE(client, auth_headers):
  id = 1

  response = client.delete(f'{endpoint}/{id}')
  assert is_valid(response, 401) # UNAUTHORIZED - Missing Authorization Header

  response = client.delete(f'{endpoint}/{id}', headers=auth_headers["pending"])
  assert is_valid(response, 200) # OK - Ticket Removed from Database

  # TODO: A request to delete a non-existent ticket should return a 404 status
  # response = client.delete(f'{endpoint}/{id}', headers=auth_headers["admin"])
  # assert is_valid(response, 404) # NOT FOUND - Emergency Contact not found

# TODO: Potential problem - Pending users have access to delete, modify, and add tickets...