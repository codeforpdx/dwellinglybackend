import pytest
from models.staff_tenant_link import StaffTenantLink


def assigned(tenant, staff):
    return (
        len(
            StaffTenantLink.query.filter(
                StaffTenantLink.tenant_id == tenant.id,
                StaffTenantLink.staff_id == staff.id,
            ).all()
        )
        == 1
    )


def test_assigned(empty_test_db, create_tenant, create_join_staff):
    tenant = create_tenant()
    staff = create_join_staff()
    StaffTenantLink(tenant_id=tenant.id, staff_id=staff.id).save_to_db()

    assert assigned(tenant, staff)

    assert not assigned(create_tenant(), staff)


def valid_payload(tenants, staff):
    return {"staff": staff, "tenants": tenants}


def endpoint():
    return "/api/staff-tenants"


@pytest.mark.usefixtures("client_class", "empty_test_db")
class TestStaffTenant:
    def test_when_provided_no_staff_params(
        self, valid_header, create_tenant, create_join_staff
    ):
        tenant_1 = create_tenant()
        tenant_2 = create_tenant()
        keep_tenant = create_tenant()
        StaffTenantLink(
            tenant_id=tenant_1.id, staff_id=create_join_staff().id
        ).save_to_db()
        StaffTenantLink(
            tenant_id=tenant_1.id, staff_id=create_join_staff().id
        ).save_to_db()
        StaffTenantLink(
            tenant_id=tenant_2.id, staff_id=create_join_staff().id
        ).save_to_db()
        StaffTenantLink(
            tenant_id=keep_tenant.id, staff_id=create_join_staff().id
        ).save_to_db()

        assert len(StaffTenantLink.query.all()) == 4

        def should_delete_all_rows_with_provided_tenant_ids():
            return self.client.patch(
                endpoint(),
                json=valid_payload(tenants=[tenant_1.id, tenant_2.id], staff=[]),
                headers=valid_header,
            )

        response = should_delete_all_rows_with_provided_tenant_ids()
        assert response.status_code == 200
        assert response.json == {
            "message": "Staff-Tenant associations updated successfully"
        }
        assert len(StaffTenantLink.query.all()) == 1

    def test_when_provided_staff_params(
        self, valid_header, create_tenant, create_join_staff
    ):
        tenant = create_tenant()
        old_staff = create_join_staff()
        StaffTenantLink(tenant_id=tenant.id, staff_id=old_staff.id).save_to_db()

        new_staff = create_join_staff()

        assert len(StaffTenantLink.query.all()) == 1
        assert assigned(tenant, old_staff)

        def should_remove_old_staff_and_add_new_staff():
            return self.client.patch(
                endpoint(),
                json=valid_payload(tenants=[tenant.id], staff=[new_staff.id]),
                headers=valid_header,
            )

        response = should_remove_old_staff_and_add_new_staff()
        assert response.status_code == 200
        assert response.json == {
            "message": "Staff-Tenant associations updated successfully"
        }
        assert len(StaffTenantLink.query.all()) == 1
        assert assigned(tenant, new_staff)
        assert not assigned(tenant, old_staff)

    def test_bulk_update(self, valid_header, create_tenant, create_join_staff):
        tenant_1 = create_tenant()
        tenant_2 = create_tenant()
        tenant_3 = create_tenant()
        staff_1 = create_join_staff()
        staff_2 = create_join_staff()
        staff_3 = create_join_staff()

        StaffTenantLink(tenant_id=tenant_1.id, staff_id=staff_1.id).save_to_db()
        StaffTenantLink(tenant_id=tenant_1.id, staff_id=staff_2.id).save_to_db()
        StaffTenantLink(tenant_id=tenant_2.id, staff_id=staff_1.id).save_to_db()
        StaffTenantLink(tenant_id=tenant_2.id, staff_id=staff_3.id).save_to_db()

        staff_tenants = StaffTenantLink.query.all()
        assert len(staff_tenants) == 4
        assert assigned(tenant_1, staff_1)
        assert assigned(tenant_1, staff_2)
        assert assigned(tenant_2, staff_1)
        assert assigned(tenant_2, staff_3)

        def all_provided_tenants_should_be_updated():
            return self.client.patch(
                endpoint(),
                json=valid_payload(
                    tenants=[tenant_1.id, tenant_2.id, tenant_3.id],
                    staff=[staff_2.id, staff_3.id],
                ),
                headers=valid_header,
            )

        response = all_provided_tenants_should_be_updated()
        assert response.status_code == 200
        assert response.json == {
            "message": "Staff-Tenant associations updated successfully"
        }
        staff_tenants = StaffTenantLink.query.all()
        assert len(staff_tenants) == 6
        assert assigned(tenant_1, staff_2)
        assert assigned(tenant_1, staff_3)
        assert assigned(tenant_2, staff_2)
        assert assigned(tenant_2, staff_3)
        assert assigned(tenant_3, staff_2)
        assert assigned(tenant_3, staff_3)
        assert not assigned(tenant_1, staff_1)
        assert not assigned(tenant_2, staff_1)

    def test_invalid_payload(self, valid_header):
        response = self.client.patch(endpoint(), json={}, headers=valid_header)

        assert response.status_code == 400
