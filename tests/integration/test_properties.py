import pytest
import json
from models.property import PropertyModel
from models.user import UserModel
from models.tenant import TenantModel


def test_get_properties(client, test_database):
    """the server should successfully retrieve all properties"""
    response = client.get("/api/properties")
    assert response.status_code == 200


def test_post_property(
    client, auth_headers, property_attributes, create_property_manager
):
    property_attrs = property_attributes()

    """The server should successfully add a new property"""
    response = client.post(
        "/api/properties", json=property_attrs, headers=auth_headers["admin"]
    )
    assert response.status_code == 201

    """The server should return with an error if a duplicate property is posted"""
    response = client.post(
        "/api/properties", json=property_attrs, headers=auth_headers["admin"]
    )
    assert response.get_json() == {
        "message": {"name": ["A property with this name already exists"]}
    }
    assert response.status_code == 400


def test_get_property_by_id(client, auth_headers, test_database):
    """The get property by name returns a successful response code."""
    response = client.get("/api/properties/1", headers=auth_headers["admin"])
    property_info = response.get_json()
    user_json = UserModel.find(5).json()
    assert response.status_code == 200
    assert property_info["name"] == "test1"
    assert property_info["address"] == "123 NE FLanders St"
    assert property_info["num_units"] == 5
    assert property_info["city"] == "Portland"
    assert property_info["state"] == "OR"
    assert property_info["zipcode"] == "97207"
    assert property_info["propertyManager"] == [user_json]
    assert property_info["propertyManagerName"] == ["Gray Pouponn"]
    assert property_info["archived"] == 0
    assert property_info["tenants"] == [TenantModel.find(1).json()]

    """
    The server responds with an error if the URL contains a non-existent property id
    """
    responseBadPropertyName = client.get(
        "/api/properties/23", headers=auth_headers["admin"]
    )
    assert responseBadPropertyName == 404
    assert responseBadPropertyName.json == {"message": "Property not found"}


def test_archive_property_by_id(client, auth_headers, create_property, test_database):
    test_property = create_property()

    """The server responds with a 401 error if a non-admin tries to archive"""
    responseNoAdmin = client.post(f"/api/properties/archive/{test_property.id}")
    assert responseNoAdmin == 401
    assert responseNoAdmin.json == {"message": "Missing authorization header"}

    """The archive property endpoint should return a 200 code when successful"""
    responseSuccess = client.post(
        f"/api/properties/archive/{test_property.id}", headers=auth_headers["admin"]
    )
    assert responseSuccess.status_code == 200

    """The property should have its 'archived' key set to True"""
    responseArchivedProperty = client.get(
        f"/api/properties/{test_property.id}", headers=auth_headers["admin"]
    )
    assert json.loads(responseArchivedProperty.data)["archived"]


@pytest.mark.usefixtures("client_class", "empty_test_db")
class TestPropertyArchivalMethods:
    def test_archive_properties_non_admin(self, staff_header):
        """The server responds with a 401 error if a non-admin tries to archive"""
        responseNoAdmin = self.client.patch(
            "/api/properties/archive", json={}, headers=staff_header
        )
        assert responseNoAdmin == 401

    def test_archive_properties(self, admin_header, create_property):
        firstProperty = create_property()
        secondProperty = create_property()
        thirdProperty = create_property()
        propertiesInfo = [firstProperty, secondProperty, thirdProperty]
        firstPropertyId = firstProperty.id
        allPropertyIds = [p.id for p in propertiesInfo]

        """The archive properties endpoint should return a 201 code when successful"""
        responseSuccess = self.client.patch(
            "/api/properties/archive",
            json={"ids": [firstPropertyId]},
            headers=admin_header,
        )
        assert responseSuccess.status_code == 200

        """
        The archive properties endpoint should return data for all properties
        (check count, spot-check some fields) when successful
        """
        responseSuccess = self.client.patch(
            "/api/properties/archive",
            json={"ids": [firstPropertyId]},
            headers=admin_header,
        )
        propertiesReturnedByEndpoint = json.loads(responseSuccess.data)["properties"]
        assert len(propertiesReturnedByEndpoint) == len(propertiesInfo)
        assert all([p["name"] and p["address"] for p in propertiesReturnedByEndpoint])

        """The (single) archived property has its 'archived' key set to True"""
        response = self.client.get(
            f"/api/properties/{firstProperty.id}", headers=admin_header
        )
        assert json.loads(response.data)["archived"]

        """
        When archiving multiple properties,
        all properties have the 'archived' key set to True
        """
        responseSuccess = self.client.patch(
            "/api/properties/archive",
            json={"ids": allPropertyIds},
            headers=admin_header,
        )
        responseAllProperties = self.client.get("/api/properties", headers=admin_header)
        assert all(
            [
                prop["archived"]
                for prop in json.loads(responseAllProperties.data)["properties"]
            ]
        )

        """
        The server responds with a 400 error if request body
        does not contain a list of property ids
        """
        responseBadPropertyID = self.client.patch(
            "/api/properties/archive", json={}, headers=admin_header
        )
        assert responseBadPropertyID.get_json() == {
            "message": "Property IDs missing in request"
        }
        assert responseBadPropertyID.status_code == 400


def test_delete_property_by_id(client, auth_headers, test_database):
    test_property = PropertyModel.find_by_name("The Reginald")

    """First verify that the property exists"""
    response = client.get(
        f"/api/properties/{test_property.id}", headers=auth_headers["admin"]
    )
    assert response.status_code == 200

    response = client.delete(
        f"/api/properties/{test_property.id}", headers=auth_headers["admin"]
    )
    assert response.status_code == 200
    assert response.json == {"message": "Property deleted"}

    """Now verify that the property no longer exists"""
    response = client.get(
        f"/api/properties/{test_property.id}", headers=auth_headers["admin"]
    )
    assert response.status_code == 404
    assert response.json == {"message": "Property not found"}

    """The server responds with a 401 error if a non-admin tries to delete"""
    responseNoAdmin = client.delete(f"/api/properties/{test_property.id}")
    assert responseNoAdmin == 401
    assert responseNoAdmin.json == {"message": "Missing authorization header"}

    """The server responds with a 404 error if property not exist"""
    response = client.delete("/api/properties/23", headers=auth_headers["admin"])
    assert response == 404


def test_update_property(client, empty_test_db, valid_header, create_property):
    test_property = create_property()
    new_property_address = "123 NE Flanders St"

    property_json = test_property.json()

    property_json["address"] = new_property_address

    """
    Updating property info should be successful when the payload includes
    the property's current name. The response JSON should reflect these changes.
    """
    response = client.put(
        f"/api/properties/{test_property.id}",
        json=property_json,
        headers=valid_header,
    )
    assert response == 200
    assert response.json == property_json

    new_property = create_property()
    duplicate_name = test_property.name

    new_property_json = new_property.json()
    new_property_json["name"] = duplicate_name

    """
    The server responds with a 400 error when attempting to update a
    property with the name of another existing property.
    """
    response = client.put(
        f"/api/properties/{new_property.id}",
        json=new_property_json,
        headers=valid_header,
    )
    assert response == 400
