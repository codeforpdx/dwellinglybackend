import pytest
import json
from unittest.mock import patch
from schemas.property import PropertySchema
from models.property import PropertyModel


@pytest.mark.usefixtures("client_class", "empty_test_db")
class TestProperty:
    def setup(self):
        self.endpoint = "/api/properties/"

    def test_get(self, valid_header, create_property):
        property = create_property()
        response = self.client.get(
            f"{self.endpoint}{property.id}", headers=valid_header
        )

        assert response.json == property.json(include_tenants=True)

    def test_delete(self, valid_header, create_property):
        with patch.object(PropertyModel, "delete") as mock_delete:
            response = self.client.delete(f"{self.endpoint}1", headers=valid_header)

        mock_delete.assert_called_once_with(1)
        assert response.status_code == 200
        assert response.json == {"message": "Property deleted"}

    def test_put(self, valid_header, create_property):
        property = create_property()

        with patch.object(
            PropertyModel, "update", return_value=property
        ) as mock_update:
            response = self.client.put(
                f"{self.endpoint}1", json={"num_units": 2}, headers=valid_header
            )

        mock_update.assert_called_once_with(
            schema=PropertySchema,
            id=1,
            context={"name": property.name},
            payload={"num_units": 2},
        )
        assert response.status_code == 200
        assert response.json == property.json()


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


def test_archive_property_by_id(client, auth_headers, create_property, test_database):
    test_property = create_property()

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
