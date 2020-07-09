from models.property import PropertyModel

def test_get_properties(client, seeded_database):
    """the server should successfully retrieve all properties"""
    response = client.get("/api/properties")
    assert response.status_code == 200
    
def test_post_property(client, admin_auth_header, new_property):
    """The server should check for the correct credentials when posting a new property"""
    response = client.post("/api/properties", json=new_property.json())
    assert response.status_code == 401
    
    """The server should successfully add a new property"""
    response = client.post("/api/properties", json=new_property.json(), headers=admin_auth_header)
    assert response.status_code == 201

    """The server should return with an error if a duplicate property is posted"""
    response = client.post("/api/properties", json=new_property.json(), headers=admin_auth_header)
    assert response.status_code == 401
    
def test_get_property_by_name(client, admin_auth_header, seeded_database):
    """The get property by name returns a successful response code."""
    response = client.get("/api/properties/test1", headers=admin_auth_header)
    assert response.status_code == 200

    """The server responds with an error if the URL containts a non-existent property name"""
    responseBadPropertyName = client.get("/api/properties/this_property_does_not_exist", headers=admin_auth_header)
    assert responseBadPropertyName == 404

def test_get_property_by_id(client, admin_auth_header, new_property, seeded_database):
    """The get property by id returns a successful response code."""
    test_property = PropertyModel.find_by_name(new_property.name)
    response = client.get(f'/api/properties/{test_property.id}', headers=admin_auth_header)
    assert response.status_code == 200

    """The server responds with an error if the URL containts a non-existent property id"""
    responseBadPropertyName = client.get("/api/properties/000000", headers=admin_auth_header)
    assert responseBadPropertyName == 404


    