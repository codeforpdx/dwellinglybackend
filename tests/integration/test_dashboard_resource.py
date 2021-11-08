import pytest


@pytest.mark.usefixtures("client_class")
class TestDashboardResource:
    def test_GET(self, valid_header):
        response = self.client.get("/api/dashboard", headers=valid_header)

        assert response.status_code == 200
