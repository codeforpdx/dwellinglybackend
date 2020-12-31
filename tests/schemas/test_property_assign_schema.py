from schemas.property_assignment import PropertyAssignSchema


class TestPropertyAssignSchemaValidation:
    def test_foreign_key_constraints(self, empty_test_db):
        validation = PropertyAssignSchema().validate(
            {"manager_id": 23, "property_id": 22}
        )
        assert "manager_id", "property_id" in validation

    def test_manager_id_is_property_manager_pk(self, empty_test_db, create_join_staff):
        invalid_data = {"manager_id": create_join_staff().id, "property_id": 3}
        validation_error = PropertyAssignSchema().validate(invalid_data)
        assert "manager_id", "property_id" in validation_error
