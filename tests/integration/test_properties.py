import pytest
import json
from unittest.mock import patch
from schemas.property import PropertySchema
from models.property import PropertyModel


@pytest.mark.usefixtures("client_class", "empty_test_db")
class TestPropertyGet:
    def test_get(self, valid_header, create_property):
        property = PropertyModel()
        json = {"key": "value"}

        with patch.object(PropertyModel, "find", return_value=property) as mock_find:
            with patch.object(property, "json", return_value=json) as mock_json:
                response = self.client.get("/api/properties/7", headers=valid_header)

        mock_find.assert_called_once_with(7)
        mock_json.assert_called_once_with(include_tenants=True)
        assert response.json == json
        assert response.status_code == 200


@pytest.mark.usefixtures("client_class", "empty_test_db")
class TestPropertyDelete:
    def test_delete(self, valid_header, create_property):
        with patch.object(PropertyModel, "delete") as mock_delete:
            response = self.client.delete("/api/properties/1", headers=valid_header)

        mock_delete.assert_called_once_with(1)
        assert response.status_code == 200
        assert response.json == {"message": "Property deleted"}


@pytest.mark.usefixtures("client_class", "empty_test_db")
class TestPropertyPut:
    def test_put(self, valid_header, create_property):
        property = create_property()

        with patch.object(
            PropertyModel, "update", return_value=property
        ) as mock_update:
            response = self.client.put(
                "/api/properties/1", json={"num_units": 2}, headers=valid_header
            )

        mock_update.assert_called_once_with(
            schema=PropertySchema,
            id=1,
            context={"name": property.name},
            payload={"num_units": 2},
        )
        assert response.status_code == 200
        assert response.json == property.json()


@pytest.mark.usefixtures("client_class", "empty_test_db")
class TestPropertiesGet:
    def test_get(self, valid_header, create_property):
        property = create_property()
        response = self.client.get("/api/properties", headers=valid_header)

        assert response.json == {"properties": [property.json()]}
        assert response.status_code == 200


@pytest.mark.usefixtures("client_class", "empty_test_db")
class TestPropertiesPost:
    def test_post(self, valid_header, property_attributes):
        property_attrs = property_attributes()
        property = PropertyModel()
        json = {"key": "value"}

        with patch.object(
            PropertyModel, "create", return_value=property
        ) as mock_create:
            with patch.object(property, "json", return_value=json) as mock_json:
                response = self.client.post(
                    "/api/properties", json=property_attrs, headers=valid_header
                )

        mock_create.assert_called_once_with(
            schema=PropertySchema,
            payload=property_attrs,
        )
        mock_json.assert_called()
        assert response.json == json
        assert response.status_code == 201


@pytest.mark.usefixtures("client_class", "empty_test_db")
class TestPropertyArchivalMethods:
    def test_archive_properties(self, valid_header, create_property):
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
            headers=valid_header,
        )
        assert responseSuccess.status_code == 200

        """
        The archive properties endpoint should return data for all properties
        (check count, spot-check some fields) when successful
        """
        responseSuccess = self.client.patch(
            "/api/properties/archive",
            json={"ids": [firstPropertyId]},
            headers=valid_header,
        )
        propertiesReturnedByEndpoint = json.loads(responseSuccess.data)["properties"]
        assert len(propertiesReturnedByEndpoint) == len(propertiesInfo)
        assert all([p["name"] and p["address"] for p in propertiesReturnedByEndpoint])
        assert firstProperty.archived

        """
        When archiving multiple properties,
        all properties have the 'archived' key set to True
        """
        responseSuccess = self.client.patch(
            "/api/properties/archive",
            json={"ids": allPropertyIds},
            headers=valid_header,
        )
        responseAllProperties = self.client.get("/api/properties", headers=valid_header)
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
            "/api/properties/archive", json={}, headers=valid_header
        )
        assert responseBadPropertyID.get_json() == {
            "message": "Property IDs missing in request"
        }
        assert responseBadPropertyID.status_code == 400

    def test_archive_property_by_id(self, valid_header, create_property):
        test_property = create_property()

        """The archive property endpoint should return a 200 code when successful"""
        responseSuccess = self.client.post(
            f"/api/properties/archive/{test_property.id}", headers=valid_header
        )
        assert responseSuccess.status_code == 200
        assert test_property.archived
