import pytest


@pytest.mark.usefixtures("client_class", "empty_test_db")
class TestWidgets:
    def setup(self):
        self.password = "strongestpasswordever"

    def test_get_widgets(self, valid_header):
        widget_response = self.client.get("/api/widgets", headers=valid_header)

        assert widget_response.status_code == 200
        widgetJson = widget_response.json
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
