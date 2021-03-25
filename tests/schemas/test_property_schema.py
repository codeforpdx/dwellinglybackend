import pytest
from schemas import PropertySchema


@pytest.mark.usefixtures("empty_test_db")
class TestPropertyValidations:
    def test_valid_payload(self, create_property_manager, property_attributes):

        valid_payload = property_attributes()
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

    def test_property_can_update_with_same_name(self, create_property):
        new_property = create_property()
        payload = new_property.json()

        payload["num_units"] = 42

        context = {"name": new_property.name}

        validation_errors = PropertySchema(context=context).validate(payload)

        assert "name" not in validation_errors

    def test_updated_property_cannot_have_duplicate_name(self, create_property):
        property_1 = create_property()
        property_2 = create_property()

        payload = property_1.json()
        payload["name"] = property_2.name

        context = {"name": property_1.name}

        validation_errors = PropertySchema(context=context).validate(payload)

        assert "name" in validation_errors


@pytest.mark.usefixtures("empty_test_db")
class TestPostLoadDeserialization:
    def test_property_created_with_manager_ids(
        self, property_attributes, create_property_manager
    ):
        pm_1 = create_property_manager()
        pm_2 = create_property_manager()
        property_attrs = property_attributes(manager_ids=[pm_1.id, pm_2.id])

        prop = PropertySchema().load(property_attrs)

        assert prop
        assert prop["managers"] == [pm_1, pm_2]

    def test_manager_update(self, create_property, create_property_manager):
        prop = create_property()
        pm_2 = create_property_manager()
        pm_3 = create_property_manager()
        payload = {"propertyManagerIDs": [pm_2.id, pm_3.id]}
        context = {"name": prop.name}

        updated_prop = PropertySchema(context=context).load(payload, partial=True)

        assert updated_prop["managers"] == [pm_2, pm_3]

    def test_property_update_without_managers(self, create_property):
        prop = create_property()
        payload = {
            "name": "The New Portlander Delux Apartment Complex Multnomah Suites",
        }
        context = {"name": prop.name}

        assert PropertySchema(context=context).load(payload, partial=True)
