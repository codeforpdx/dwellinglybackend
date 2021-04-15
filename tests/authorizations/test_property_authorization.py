import pytest


@pytest.mark.usefixtures("client_class", "empty_test_db")
class TestPropertyAuthorizations:
    def test_post_property(self, property_attributes):
        property_attrs = property_attributes()

        """
        The server should check for the correct credentials when posting a new property
        """
        response = self.client.post("/api/properties", json=property_attrs)
        assert response.status_code == 401

    def test_delete_property_by_id(self, create_property):
        test_property = create_property()

        """The server responds with a 401 error if a non-admin tries to delete"""
        responseNoAdmin = self.client.delete(f"/api/properties/{test_property.id}")
        assert responseNoAdmin == 401
        assert responseNoAdmin.json == {"message": "Missing authorization header"}

    def test_archive_property_by_id(self, create_property):
        test_property = create_property()

        """The server responds with a 401 error if a non-admin tries to archive"""
        responseNoAdmin = self.client.post(
            f"/api/properties/archive/{test_property.id}"
        )
        assert responseNoAdmin == 401
        assert responseNoAdmin.json == {"message": "Missing authorization header"}

    def test_archive_properties_non_admin(self, staff_header):
        """The server responds with a 401 error if a non-admin tries to archive"""
        responseNoAdmin = self.client.patch(
            "/api/properties/archive", json={}, headers=staff_header
        )
        assert responseNoAdmin == 401
