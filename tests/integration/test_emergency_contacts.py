from models.emergency_contact import EmergencyContactModel
from conftest import login_user

endpoint = '/api/emergencycontacts'

# QUESTIONS
# 1. Is it ok to use data from the seeded_database for testing?
# 2. Should each route be tested for appropriate auth-based rejections?

def test_emergency_contacts_GET_all(client, test_database):
  response = client.get(endpoint)
  assert response.status_code == 200
  assert response.json['emergency_contacts'][0]['name'] == 'Narcotics Anonymous'


def test_emergency_contacts_GET_one(client, test_database):
  id = 1
  response = client.get(f'{endpoint}/{id}')
  assert response.status_code == 200
  assert response.json['name'] == 'Narcotics Anonymous'

def test_emergency_contacts_POST(client, test_database, admin_user):
  login_response, auth_header = login_user(client, admin_user)
  newContact = {
    'name': "Narcotics Anonymous",
    'description': "Cool description",
    'contact_numbers': [
      {"number": "503-291-9111", "numtype": "Call"},
      {"number": "503-555-3321", "numtype": "Text"}
    ]
  }
  response = client.post(endpoint, json=newContact, headers=auth_header)
  assert response.status_code == 401 # UNAUTHORIZED - An emergency contact with this name already exists

  newContact['name'] = "Cooler Name"
  response = client.post(endpoint, json=newContact, headers=auth_header)
  assert response.status_code == 201 # CREATED


def test_emergency_contacts_PUT(client, test_database, admin_user):
  login_response, auth_header = login_user(client, admin_user)
  id = 1
  updatedInfo = {
    'name': 'Cooler Name',
    'contact_numbers': [
      {"number": "503-291-9111", "numtype": "Call"},
      {"number": "503-555-3321", "numtype": "Text"}
    ]
  }
  response = client.put(f'{endpoint}/{id}', json=updatedInfo, headers=auth_header)
  assert response.status_code == 200 # OK


def test_emergency_contacts_DELETE(client, test_database, admin_user):
  login_response, auth_header = login_user(client, admin_user)
  id = 1
  response = client.delete(f'{endpoint}/{id}', headers=auth_header)
  assert response.status_code == 200 # OK - Emergency Contact Deleted
  response = client.get(f'{endpoint}/{id}')
  assert response.status_code == 404 # NOT FOUND - Emergency Contact not found


# A debug function that prints useful response data
# Be sure to run "pytest -s" to allow console prints
def pr(response):
  print(f'\n\nResponse Status: {response.status}')
  print(f'Response JSON: {response.json}\n')