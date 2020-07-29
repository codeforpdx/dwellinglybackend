from models.property import PropertyModel
import json

def test_get_properties(client, test_database):
    """the server should successfully retrieve all properties"""
    response = client.get("/api/properties")
    assert response.status_code == 200
    
def test_post_property(client, auth_headers, new_property):
    """The server should check for the correct credentials when posting a new property"""
    response = client.post("/api/properties", json=new_property.json())
    assert response.status_code == 401
    
    """The server should successfully add a new property"""
    response = client.post("/api/properties", json=new_property.json(), headers=auth_headers["admin"])
    assert response.status_code == 201

    """The server should return with an error if a duplicate property is posted"""
    response = client.post("/api/properties", json=new_property.json(), headers=auth_headers["admin"])
    assert response.status_code == 401
    
def test_get_property_by_name(client, auth_headers, test_database):
    """The get property by name returns a successful response code."""
    response = client.get("/api/properties/test1", headers=auth_headers["admin"])
    assert response.status_code == 200

    """The server responds with an error if the URL contains a non-existent property name"""
    responseBadPropertyName = client.get("/api/properties/this_property_does_not_exist", headers=auth_headers["admin"])
    assert responseBadPropertyName == 404

def test_get_property_by_id(client, auth_headers, new_property, test_database):
    test_property = PropertyModel.find_by_name(new_property.name)

    """The get property by id returns a successful response code."""
    response = client.get(f'/api/properties/{test_property.id}', headers=auth_headers["admin"])
    assert response.status_code == 200

    """The server responds with an error if the URL contains a non-existent property id"""
    responseBadPropertyName = client.get("/api/properties/000000", headers=auth_headers["admin"])
    assert responseBadPropertyName == 404

def test_archive_property_by_id(client, auth_headers, new_property, test_database):
    test_property = PropertyModel.find_by_name(new_property.name)

    """The server responds with a 401 error if a non-admin tries to archive"""
    responseNoAdmin = client.post(f"/api/properties/archive/{test_property.id}")
    assert responseNoAdmin == 401

    """The archive property endpoint should return a 201 code when successful"""
    responseSuccess = client.post(f'/api/properties/archive/{test_property.id}', headers=auth_headers["admin"])
    assert responseSuccess.status_code == 201
    
    """The property should have its 'archived' key set to True"""
    responseArchivedProperty = client.get(f'/api/properties/{test_property.name}', headers=auth_headers["admin"])
    assert json.loads(responseArchivedProperty.data)["archived"] 

    """The server responds with a 404 error if the URL contains a non-existent property id"""
    responseBadPropertyID = client.get("/api/properties/archive/000000", headers=auth_headers["admin"])
    assert responseBadPropertyID == 405

def test_delete_property_by_name(client, auth_headers, new_property, test_database):
    test_property = PropertyModel.find_by_name(new_property.name)

    """First verify that the property exists"""
    response = client.get(f"/api/properties/{test_property.name}", headers=auth_headers["admin"])
    assert response.status_code == 200

    response = client.delete(f"/api/properties/{test_property.name}", headers=auth_headers["admin"])
    assert response.status_code == 200

    """Now verify that the property no longer exists"""
    response = client.get(f"/api/properties/{test_property.name}", headers=auth_headers["admin"])
    assert response.status_code == 404

    """The server responds with a 401 error if a non-admin tries to delete"""
    responseNoAdmin = client.delete(f"/api/properties/{test_property.name}")
    assert responseNoAdmin == 401

def test_update_property_by_name(client, auth_headers, new_property, test_database):
    test_property = PropertyModel.find_by_name(new_property.name)
    new_property_address = "123 NE Flanders St"
    test_property.address = new_property_address
    responseUpdateProperty = client.put( f'/api/properties/{test_property.id}'
                                       , headers=auth_headers["admin"]
                                       , json=test_property.json()
                                       )

    """The property should have a new address"""
    test_changed_property = client.get(f'/api/properties/{test_property.name}', headers=auth_headers["admin"])
    test_changed_property = json.loads(test_changed_property.data)
    
    assert test_changed_property["address"] == new_property_address

