import pytest


@pytest.mark.usefixtures("client_class")
class TestWidgets:
    def test_get_widgets(self, valid_header):
        response = self.client.get("/api/widgets", headers=valid_header)

        assert response.status_code == 200
