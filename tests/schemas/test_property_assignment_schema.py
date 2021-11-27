from schemas.property_assignment import PropertyAssignmentSchema


class TestPropertyAssignmentSchemaValidation:
    def test_foreign_key_constraints(self):
        validation = PropertyAssignmentSchema().validate(
            {"manager_id": 23, "property_id": 22}
        )
        assert "manager_id", "property_id" in validation

    def test_manager_id_is_property_manager_pk(self, create_join_staff):
        invalid_data = {"manager_id": create_join_staff().id, "property_id": 3}
        validation_error = PropertyAssignmentSchema().validate(invalid_data)
        assert "manager_id", "property_id" in validation_error
