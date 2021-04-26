from conftest import is_valid

endpoint = "/api/tickets"
validTicketID = 1
invalidTicketID = 777


def test_notes_POST(client, auth_headers):
    newNote = {"text": "We don't need no water"}

    response = client.post(
        f"{endpoint}/{validTicketID}/notes", json=newNote, headers=auth_headers["admin"]
    )
    assert is_valid(response, 200)
    assert response.json["id"] != 0
    assert response.json["id"] == 5
    assert response.json["ticketid"] == 1
    assert response.json["text"] == "We don't need no water"
    assert response.json["user"] == "user4 admin"

    response = client.post(
        f"{endpoint}/{invalidTicketID}/notes",
        json=newNote,
        headers=auth_headers["admin"],
    )

    assert is_valid(response, 400)  # Bad Request- 'Invalid Ticket'
