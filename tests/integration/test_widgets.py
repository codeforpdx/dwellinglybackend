import pytest


@pytest.mark.usefixtures("client_class", "empty_test_db")
class TestWidgets:
    def test_get_widgets(self, valid_header):
        response = self.client.get("/api/widgets", headers=valid_header)

        assert response.status_code == 200
