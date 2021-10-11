import pytest


@pytest.mark.usefixtures("client_class", "empty_test_db")
class TestWidgets:
    def setup(self):
        self.password = "strongestpasswordever"

    def test_get_widgets(self, create_admin_user):
        user = create_admin_user(pw=self.password)
        response = self.client.post(
            "/api/login",
            json={"email": user.email, "password": self.password},
        )
        header = {"Authorization": f"Bearer {response.json['access_token']}"}
        widgetResponse = self.client.get("/api/widgets", headers=header)

        assert widgetResponse.status_code == 200
        widgetJson = widgetResponse.json
        assert len(widgetJson["opentickets"]) == 2
        assert len(widgetJson["managers"]) == 0

        # check for correct keys for new tickets
        assert "new" in widgetJson["opentickets"]
        assert "allNew" in widgetJson["opentickets"]["new"]
        assert "unseen24Hrs" in widgetJson["opentickets"]["new"]

        # check for correct keys for in-progress tickets
        assert "inProgress" in widgetJson["opentickets"]
        assert "allInProgress" in widgetJson["opentickets"]["inProgress"]
        assert "inProgress1Week" in widgetJson["opentickets"]["inProgress"]
