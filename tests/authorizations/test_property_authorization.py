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
