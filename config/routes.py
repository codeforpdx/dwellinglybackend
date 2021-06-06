from flask_restful import Api
from resources.user import (
    UserRegister,
    User,
    UserLogin,
    ArchiveUser,
    UsersRole,
    UserAccessRefresh,
    UserRoles,
    Users,
)
from resources.user_invite import UserInvite
from resources.users.pending_users import UsersPending
from resources.reset_password import ResetPassword
from resources.property import Properties, Property, ArchiveProperty, ArchiveProperties
from resources.staff_tenants import StaffTenants
from resources.tenants import Tenants, Tenant
from resources.emergency_contacts import EmergencyContacts
from resources.email import Email
from resources.tickets import Ticket, Tickets
from resources.notes import Note
from resources.lease import Lease, Leases
from resources.widgets import Widgets


class Routes:
    @staticmethod
    def routing(app):
        api = Api(app, prefix="/api/")
        api.add_resource(UserRegister, "register")
        api.add_resource(Property, "properties/<int:id>")
        api.add_resource(Properties, "properties")
        api.add_resource(ArchiveProperties, "properties/archive")
        api.add_resource(ArchiveProperty, "properties/archive/<int:id>")
        api.add_resource(User, "user/<int:user_id>")
        api.add_resource(UserInvite, "user/invite")
        api.add_resource(Users, "user")
        api.add_resource(UsersRole, "users/role")
        api.add_resource(UsersPending, "users/pending")
        api.add_resource(ArchiveUser, "user/archive/<int:user_id>")
        api.add_resource(UserLogin, "login")
        api.add_resource(UserRoles, "roles")
        api.add_resource(Widgets, "widgets")
        api.add_resource(Email, "user/message")
        api.add_resource(UserAccessRefresh, "refresh")
        api.add_resource(StaffTenants, "staff-tenants")
        api.add_resource(Tenants, "tenants")
        api.add_resource(Tenant, "tenants/<int:id>")
        api.add_resource(
            EmergencyContacts, "emergencycontacts", "emergencycontacts/<int:id>"
        )
        api.add_resource(Lease, "lease/<int:id>")
        api.add_resource(Leases, "lease")
        api.add_resource(Tickets, "tickets")
        api.add_resource(Ticket, "tickets/<int:id>")
        api.add_resource(Note, "tickets/<int:id>/notes")
        api.add_resource(
            ResetPassword, "reset-password", "reset-password/<string:token>"
        )
