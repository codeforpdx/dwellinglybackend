from flask_restful import Resource
from flask import request
from db import db
from schemas.staff_tenants import StaffTenantSchema
from models.staff_tenant_link import StaffTenantLink
from utils.authorizations import admin_required


class StaffTenants(Resource):
    @admin_required
    def patch(self):
        data = StaffTenantLink.validate(StaffTenantSchema, request.json)

        StaffTenantLink.query.filter(
            StaffTenantLink.tenant_id.in_(data['tenants'])
        ).delete(synchronize_session='fetch')

        staff_tenants = []
        for tenant_id in data['tenants']:
            for staff_id in data['staff']:
                staff_tenants.append(StaffTenantLink(tenant_id=tenant_id, staff_id=staff_id))

        db.session.bulk_save_objects(staff_tenants)
        db.session.commit()

        return {'message': 'Staff-Tenant associations updated successfully'}
