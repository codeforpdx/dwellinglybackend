import pytest
from schemas import PropertySchema
from models.property import PropertyModel
from db import db


@pytest.mark.usefixtures("empty_test_db")
class TestPropertyManagerValidations:
    def test_valid_payload(self, create_property_manager):

        valid_payload = {
            "name": "the heights",
            "address": "111 SW Harrison",
            "city": "Portland",
            "num_units": 101,
            "state": "OR",
            "zipcode": "97207",
            "propertyManagerIDs": [create_property_manager().id],
            "archived": False,
        }
        no_validation_errors = {}
        assert no_validation_errors == PropertySchema().validate(valid_payload)

    def test_missing_required_parameters(self, create_property_manager):
        invalid_payload = {
            "unit": "101",
            "propertyManagerIDs": [create_property_manager().id],
            "archived": False,
        }
        validation_errors = PropertySchema().validate(invalid_payload)
        assert "name" in validation_errors
        assert "address" in validation_errors
        assert "city" in validation_errors
        assert "state" in validation_errors
        assert "zipcode" in validation_errors

    def test_must_have_manager_assigned(self):
        validation_error = PropertySchema().validate({"propertyManagerIDs": []})
        assert "propertyManagerIDs" in validation_error

    def test_propertyManagerIDs_are_validated(self, create_join_staff):
        staff = create_join_staff()
        validation_error = PropertySchema().validate({"propertyManagerIDs": [staff.id]})

        assert "propertyManagerIDs" in validation_error

    def test_uniqueness_of_property_name(self, create_property):
        name = create_property().name
        validation_errors = PropertySchema().validate({"name": name})

        assert "name" in validation_errors


@pytest.mark.usefixtures("empty_test_db")
class TestPostLoadDeserialization:
    def test_property_created_with_manager_ids(
        self, property_attributes, create_property_manager
    ):
        pm_1 = create_property_manager()
        pm_2 = create_property_manager()
        property_attrs = property_attributes(manager_ids=[pm_1.id, pm_2.id])

        prop = PropertyModel.create(schema=PropertySchema, payload=property_attrs)
        db.session.rollback()

        assert prop
        assert prop.managers == [pm_1, pm_2]

    def test_manager_update(self, create_property, create_property_manager):
        prop = create_property()
        pm_2 = create_property_manager()
        pm_3 = create_property_manager()
        payload = {"propertyManagerIDs": [pm_2.id, pm_3.id]}

        PropertyModel.update(schema=PropertySchema, id=prop.id, payload=payload)
        db.session.rollback()

        assert prop.managers == [pm_2, pm_3]

    def test_property_update_without_managers(self, create_property):
        prop = create_property()
        payload = {
            "name": "The New Portlander Delux Apartment Complex Multnomah Suite Express"
        }

        assert PropertyModel.update(schema=PropertySchema, id=prop.id, payload=payload)
