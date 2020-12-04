import pytest
from schemas import StaffTenantSchema
from datetime import datetime
from utils.time import Time


class TestStaffTenantValidations:
    def test_valid_payload(self, empty_test_db, create_tenant, create_join_staff):
        valid_payload = {
            'staff': [create_join_staff().id, create_join_staff().id],
            'tenants': [create_tenant().id, create_tenant().id]
        }

        no_validation_errors = {}

        assert no_validation_errors == StaffTenantSchema().validate(valid_payload)

    def test_empty_tenant_payload_is_invalid(self, empty_test_db):
        invalid_payload = {
            'staff': [],
            'tenants': []
        }

        validation_errors = StaffTenantSchema().validate(invalid_payload)

        assert 'tenants' in validation_errors
        assert validation_errors['tenants'] == ["At least one tenant ID is required"]

        assert 'staff' not in validation_errors

    def test_required_params(self, empty_test_db):
        invalid_payload = {}

        validation_errors = StaffTenantSchema().validate(invalid_payload)

        assert 'staff' in validation_errors
        assert 'tenants' in validation_errors


@pytest.mark.usefixtures('empty_test_db')
class TestForeignKeyValidations:
    def test_tenant_must_exist(self):
        validation_errors = StaffTenantSchema().validate({'tenants': ['500']})

        assert 'tenants' in validation_errors

    def test_staff_must_exist(self):
        validation_errors = StaffTenantSchema().validate({'staff': ['500']})

        assert 'staff' in validation_errors

    def test_staff_arguments_must_contain_users_with_role_staff(
            self,
            create_property_manager,
            create_tenant
        ):

        validation_errors = StaffTenantSchema().validate(
            {
                'staff': [create_property_manager().id],
                'tenants': [create_tenant().id]
            }
        )

        assert 'staff' in validation_errors
