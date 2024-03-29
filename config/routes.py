from flask_restful import Api
from resources.user import (
    UserRegister,
    User,
    UserLogin,
    ArchiveUser,
    UserAccessRefresh,
    Users,
)
from resources.user_invite import UserInvite
from resources.user_invite import PropertyManagerInviteResource
from resources.users.pending_users import UsersPending
from resources.reset_password import ResetPassword
from resources.property import Properties, Property, ArchiveProperties
from resources.staff_tenants import StaffTenants
from resources.tenants import Tenants, Tenant
from resources.emergency_contacts import EmergencyContacts, EmergencyContact
from resources.tickets import Ticket, Tickets
from resources.notes import Notes, Note
from resources.lease import Lease, Leases
from resources.dashboard_resource import DashboardResource
from tests.cypress.cypress_resource import CypressResource


class Routes:
    @staticmethod
    def routing(app):
        api = Api(app, prefix="/api/")
        api.add_resource(UserInvite, "user/invite")
        api.add_resource(PropertyManagerInviteResource, "user/invite/property_manager")
        api.add_resource(UserRegister, "register")
        api.add_resource(Property, "properties/<int:id>")
        api.add_resource(Properties, "properties")
        api.add_resource(ArchiveProperties, "properties/archive")
        api.add_resource(User, "user/<int:id>")
        api.add_resource(Users, "user")
        api.add_resource(UsersPending, "users/pending")
        api.add_resource(ArchiveUser, "user/archive/<int:user_id>")
        api.add_resource(UserLogin, "login")
        api.add_resource(DashboardResource, "dashboard")
        api.add_resource(UserAccessRefresh, "refresh")
        api.add_resource(StaffTenants, "staff-tenants")
        api.add_resource(Tenants, "tenants")
        api.add_resource(Tenant, "tenants/<int:id>")
        api.add_resource(EmergencyContacts, "emergencycontacts")
        api.add_resource(EmergencyContact, "emergencycontacts/<int:id>")
        api.add_resource(Lease, "lease/<int:id>")
        api.add_resource(Leases, "lease")
        api.add_resource(Tickets, "tickets")
        api.add_resource(Ticket, "tickets/<int:id>")
        api.add_resource(Notes, "tickets/<int:id>/notes")
        api.add_resource(Note, "tickets/<int:ticket_id>/notes/<int:id>")
        api.add_resource(
            ResetPassword, "reset-password", "reset-password/<string:token>"
        )
        api.add_resource(CypressResource, "tests/cypress")
