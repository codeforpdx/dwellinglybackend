from schemas import LeaseSchema
from datetime import datetime
from utils.time import Time


class TestLeaseValidations:
    def test_valid_payload(self, create_tenant, create_property):
        tenant = create_tenant()

        valid_payload = {
            "dateTimeStart": Time.today_iso(),
            "dateTimeEnd": Time.one_year_from_now_iso(),
            "tenantID": tenant.id,
            "propertyID": create_property().id,
        }

        no_validation_errors = {}

        assert no_validation_errors == LeaseSchema().validate(valid_payload)

    def test_dateTimeStart_is_required(self):
        validation_errors = LeaseSchema().validate({})

        assert "dateTimeStart" in validation_errors

    def test_dateTimeStart_validates_valid_format(self):
        validation_errors = LeaseSchema().validate({"dateTimeStart": Time.today_iso()})

        assert "dateTimeStart" not in validation_errors

    def test_dateTimeStart_with_invalid_format(self):
        validation_errors = LeaseSchema().validate(
            {"dateTimeStart": Time.format_date_by_year(datetime.now())}
        )

        assert "dateTimeStart" in validation_errors

    def test_dateTimeEnd_is_required(self):
        validation_errors = LeaseSchema().validate({})

        assert "dateTimeEnd" in validation_errors

    def test_dateTimeEnd_validates_valid_date_format(self):
        validation_errors = LeaseSchema().validate(
            {"dateTimeEnd": Time.one_year_from_now_iso()}
        )

        assert "dateTimeEnd" not in validation_errors

    def test_dateTimeEnd_with_invalid_date_format(self):
        validation_errors = LeaseSchema().validate(
            {"dateTimeEnd": Time.format_date_by_year(datetime.now())}
        )

        assert "dateTimeEnd" in validation_errors

    def test_created_at_is_dump_only(self):
        validation_errors = LeaseSchema().validate(
            {"created_at": Time.format_date_by_year(datetime.now())}
        )

        assert "created_at" in validation_errors

    def test_updated_at_is_dump_only(self):
        validation_errors = LeaseSchema().validate(
            {"updated_at": Time.format_date_by_year(datetime.now())}
        )

        assert "updated_at" in validation_errors

    def test_tenantID_is_required(self):
        validation_errors = LeaseSchema().validate({})

        assert "tenantID" in validation_errors

    def test_propertyID_is_required(self):
        validation_errors = LeaseSchema().validate({})

        assert "propertyID" in validation_errors


class TestForeignKeyValidations:
    def test_tenantID_must_be_valid(self):
        validation_errors = LeaseSchema().validate({"tenantID": "500"})

        assert "tenantID" in validation_errors

    def test_propertyID_must_be_valid(self):
        validation_errors = LeaseSchema().validate({"propertyID": "500"})

        assert "propertyID" in validation_errors
