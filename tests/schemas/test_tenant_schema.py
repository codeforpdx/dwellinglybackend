from datetime import datetime
from models.tenant import TenantModel
from schemas import TenantSchema
from utils.time import Time


class TestTenantValidations:
    def test_valid_payload(self, create_tenant):
        tenant = create_tenant()

        valid_payload = {
            "firstName": tenant.firstName,
            "lastName": tenant.lastName,
            "phone": tenant.phone,
        }

        no_validation_errors = {}

        assert no_validation_errors == TenantSchema().validate(valid_payload)

    def test_firstName_is_required(self):
        validation_errors = TenantSchema().validate({})

        assert "firstName" in validation_errors

    def test_lastName_is_required(self):
        validation_errors = TenantSchema().validate({})

        assert "lastName" in validation_errors

    def test_phone_is_required(self):
        validation_errors = TenantSchema().validate({})

        assert "phone" in validation_errors

    def test_firstName_max_100(self):
        long_first_name = "a" * 101
        validation_errors = TenantSchema().validate({"firstName": long_first_name})

        assert "firstName" in validation_errors

    def test_lastName_max_100(self):
        long_last_name = "a" * 101
        validation_errors = TenantSchema().validate({"lastName": long_last_name})

        assert "lastName" in validation_errors

    def test_min_length_phone_number_validation(self):
        validation_errors = TenantSchema().validate({"phone": "1234"})

        assert "phone" in validation_errors

    def test_max_length_phone_number_validation(self):
        long_phone_number = "8" * 41
        validation_errors = TenantSchema().validate({"phone": long_phone_number})

        assert "phone" in validation_errors

    def test_created_at_is_dump_only(self):
        validation_errors = TenantSchema().validate(
            {"created_at": Time.format_date_by_year(datetime.now())}
        )

        assert "created_at" in validation_errors

    def test_updated_at_is_dump_only(self):
        validation_errors = TenantSchema().validate(
            {"updated_at": Time.format_date_by_year(datetime.now())}
        )

        assert "updated_at" in validation_errors

    def test_staffIDs_are_validated(self, create_property_manager):
        pm = create_property_manager()
        validation_error = TenantSchema().validate({"staffIDs": [pm.id]})

        assert "staffIDs" in validation_error


class TestPostLoadDeserialization:
    def test_tenant_creation(
        self, tenant_attributes, create_property, create_join_staff
    ):
        staff_1 = create_join_staff()
        staff_2 = create_join_staff()

        tenant_attrs = tenant_attributes(staff=[staff_1.id, staff_2.id])

        tenant = TenantModel.create(schema=TenantSchema, payload=tenant_attrs)

        assert tenant
        assert tenant.staff == [staff_1, staff_2]
