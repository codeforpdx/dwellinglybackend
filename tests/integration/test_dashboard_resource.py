import pytest

from models.dashboard import Dashboard


@pytest.mark.usefixtures("client_class")
class TestDashboardResource:
    def test_GET(self, valid_header, create_dashboard):
        create_dashboard()
        response = self.client.get("/api/dashboard", headers=valid_header)

        assert response.status_code == 200
        assert response.json == Dashboard.json()
