import pytest
from utils.time import Time
from schemas import PropertySchema


@pytest.mark.usefixtures('empty_test_db')
class TestPropertyManagerValidations:

    def test_valid_payload(self, create_property_manager):

        valid_payload = {
            'created_at': Time.one_year_from_now(),
            'updated_at': Time.today(),
            'name': 'the heights',
            'address': '111 SW Harrison',
            'city': "Portland",
            'unit': "101",
            'state': "OR",
            'zipcode': "97207",
            'propertyManagerIDs': [create_property_manager().id],
            'archived': False
        }
        no_validation_errors = {}
        assert no_validation_errors == PropertySchema().validate(valid_payload)

    def test_must_have_manager_assigned(self):
        validation_error = PropertySchema().validate({"propertyManagerIDs": []})
        assert "propertyManagerIDs" in validation_error

    def test_uniqueness_of_property_name(self, create_property):
        name = create_property().name
        validation_errors = PropertySchema().validate({'name': name})

        assert 'name' in validation_errors
