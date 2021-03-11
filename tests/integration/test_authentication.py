from conftest import is_valid


def test_emergency_contacts_POST(client, auth_headers):
    endpoint = "/api/emergencycontacts"

    newContact = {
        "name": "Narcotics Anonymous",
        "description": "Cool description",
        "contact_numbers": [
            {"number": "503-291-9111", "numtype": "Call"},
            {"number": "503-555-3321", "numtype": "Text"},
        ],
    }

    response = client.post(endpoint, json=newContact, headers=auth_headers["pm"])
    assert is_valid(response, 401)  # UNAUTHORIZED - Admin Access Required

    response = client.post(endpoint, json=newContact)
    assert is_valid(response, 401)  # UNAUTHORIZED - Missing Authorization Header
    assert response.json == {"message": "Missing authorization header"}


def test_emergency_contacts_DELETE(client, auth_headers):
    endpoint = "/api/emergencycontacts"

    id = 1

    response = client.delete(f"{endpoint}/{id}")
    assert is_valid(response, 401)  # UNAUTHORIZED - Missing Authorization Header
    assert response.json == {"message": "Missing authorization header"}

    response = client.delete(f"{endpoint}/{id}", headers=auth_headers["pm"])
    assert is_valid(response, 401)  # UNAUTHORIZED - Admin Access Required