from models.dashboard import Dashboard


class TestDashboard:
    def test_json(self, create_dashboard):
        dashboard = create_dashboard()
        response = Dashboard.json()

        assert response == {
            "managers": [
                {
                    "date": "Today",
                    "first_name": dashboard["pm"].firstName,
                    "id": dashboard["pm"].id,
                    "last_name": dashboard["pm"].lastName,
                    "property_name": dashboard["prop"].name,
                },
                {
                    "date": "Yesterday",
                    "first_name": dashboard["pm2"].firstName,
                    "id": dashboard["pm2"].id,
                    "last_name": dashboard["pm2"].lastName,
                    "property_name": "Not Assigned",
                },
                {
                    "date": "This Week",
                    "first_name": dashboard["pm3"].firstName,
                    "id": dashboard["pm3"].id,
                    "last_name": dashboard["pm3"].lastName,
                    "property_name": dashboard["prop2"].name,
                },
            ],
            "pending_users": [dashboard["pending_user"].json()],
            "staff": [dashboard["author"].json()],
            "tenants": [dashboard["tenant"].json()],
            "tickets": {
                "new": {
                    "total_count": 7,
                    "latent_count": 2,
                },
                "in_progress": {
                    "total_count": 10,
                    "latent_count": 3,
                },
            },
        }
