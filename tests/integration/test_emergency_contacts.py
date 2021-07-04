from conftest import is_valid
import pytest

# NOTE: Each endpoint should be tested for all valid request types --
# (GET, POST, PUT, PATCH, DELETE, etc.)

# Each request should be tested to return valid:
# 1. Status Code
# 2. Headers
# 3. JSON

# Also test invalid requests, such as:
# 1. Action on non-existent entries
# 2. Duplicate creation

endpoint = "/api/emergencycontacts"


def test_emergency_contacts_GET_all(client, test_database):
    response = client.get(endpoint)
    assert is_valid(response, 200)  # OK
    assert response.json["emergency_contacts"][0]["name"] == "Narcotics Anonymous"


def test_emergency_contacts_GET_one(client, test_database):
    id = 1
    response = client.get(f"{endpoint}/{id}")
    assert is_valid(response, 200)  # OK
    assert response.json["name"] == "Narcotics Anonymous"

    id = 100
    response = client.get(f"{endpoint}/{id}")
    assert is_valid(response, 404)  # NOT FOUND - 'Emergency Contact not found'
    assert response.json == {"message": "EmergencyContact not found"}


def test_emergency_contacts_POST(test_database, client, valid_header):
    newContact = {
        "name": "Narcotics Anonymous",
        "description": "Cool description",
        "contact_numbers": [
            {"number": "503-291-9111", "numtype": "Call"},
            {"number": "503-555-3321", "numtype": "Text"},
        ],
    }

    invalidContactNum = {
        "name": "Contact Name",
        "description": "An invalid contact number",
        "contact_numbers": [
            {"number": 503 - 291 - 9111, "numtype": "Call"},
            {"number": "503-555-3321", "numtype": "Text"},
        ],
    }

    response = client.post(endpoint, json=newContact, headers=valid_header)
    assert is_valid(
        response, 400
    )  # UNAUTHORIZED - Emergency Contact With This Name Already Exists
    assert response.json == {
        "message": {"name": ["Narcotics Anonymous is already an emergency contact"]}
    }

    response = client.post(endpoint, json=invalidContactNum, headers=valid_header)
    assert is_valid(
        response, 400
    )  # BAD REQUEST - Invalid contact number - number is not string type
    assert response.json == {
        "message": {"contact_numbers": {"0": {"number": ["Not a valid string."]}}}
    }

    newContact["name"] = "Cooler Name"
    response = client.post(endpoint, json=newContact, headers=valid_header)
    assert is_valid(response, 201)  # CREATED
    assert response.json["name"] == "Cooler Name"
    assert response.json["contact_numbers"][0]["number"] == "503-291-9111"

    newContact = {}
    response = client.post(endpoint, json=newContact, headers=valid_header)
    assert is_valid(
        response, 400
    )  # BAD REQUEST - {'name': 'This Field Cannot Be Blank.'}


@pytest.mark.skip(
    reason="This is testing a successful update action on a non-existent id..."
)
def test_emergency_contacts_PUT(client, valid_header, empty_test_db):
    id = 1
    updatedInfo = {
        "name": "Greg",
        "contact_numbers": [
            {"number": "503-291-9111", "numtype": "Call"},
            {"number": "503-555-3321", "numtype": "Text"},
        ],
    }

    response = client.put(f"{endpoint}/{id}", json=updatedInfo, headers=valid_header)
    assert is_valid(response, 200)  # OK
    assert response.json["name"] == "Greg"
    # assert response.json['contact_numbers'][0]['number'] == '503-291-9111'
    # This test will fail, Contact Numbers need an id in order to be updated.
    # The request is not submitting an id.
    # TODO: Create issue to address non restful behavior.

    id = 100
    response = client.put(f"{endpoint}/{id}", json=updatedInfo, headers=valid_header)
    assert is_valid(response, 404)  # NOT FOUND
    assert response.json == {"message": "Emergency contact not found"}


def test_emergency_contacts_DELETE(test_database, client, valid_header):
    id = 1

    response = client.delete(f"{endpoint}/{id}", headers=valid_header)
    assert is_valid(response, 200)  # OK

    response = client.delete(f"{endpoint}/{id}", headers=valid_header)
    assert is_valid(response, 404)  # NOT FOUND - Emergency Contact Not Found
    assert response.json == {"message": "EmergencyContact not found"}
