import pytest
from flask import current_app
from tests.factory_fixtures.dummy_resource import DummyResource
from utils.gatekeeper import GatekeeperError


@pytest.mark.usefixtures("client_class")
class TestGatekeeper:
    def test_empty_set_allows_no_params(self):
        with pytest.raises(GatekeeperError):
            with current_app.test_request_context(json={"hi": "there"}):
                DummyResource().put()

    def test_raises_error_for_unspecified_params(self):
        DummyResource.dummy_params.update({"hello", "world"})

        with pytest.raises(GatekeeperError) as error_info:
            with current_app.test_request_context(json={"hi": "there"}):
                DummyResource().put()
        assert "Invalid request field" in str(error_info.value)

        DummyResource.dummy_params.clear()

    def test_subset_of_allowed_params_is_okay(self):
        DummyResource.dummy_params.update({"hello", "world", "again"})
        with current_app.test_request_context(json={"hello": "there"}):
            DummyResource().put()
