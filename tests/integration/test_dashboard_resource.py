import pytest


@pytest.mark.usefixtures("client_class", "empty_test_db")
class TestDashboardResource:
    def test_GET(self, valid_header):
        response = self.client.get("/api/dashboard", headers=valid_header)

        assert response.status_code == 200
