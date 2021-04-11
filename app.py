from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_mail import Mail
from models.user import UserModel

# This should not be imported here, but for now we can force Flake8 to ignore the error
# The "noqa" comment can be deleted when we figure out how to get around this.
from models.staff_tenant_link import StaffTenantLink  # noqa: F401
from models.revoked_tokens import RevokedTokensModel
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
from resources.tenants import Tenants
from resources.emergency_contacts import EmergencyContacts
from resources.email import Email
from resources.tickets import Ticket, Tickets
from resources.lease import Lease, Leases
from resources.widgets import Widgets
from db import db
from ma import ma
from manage import dbsetup
from config import app_config


def create_routes(app):
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
    api.add_resource(Tenants, "tenants", "tenants/<int:tenant_id>")
    api.add_resource(
        EmergencyContacts, "emergencycontacts", "emergencycontacts/<int:id>"
    )
    api.add_resource(Lease, "lease/<int:id>")
    api.add_resource(Leases, "lease")
    api.add_resource(Tickets, "tickets")
    api.add_resource(Ticket, "tickets/<int:id>")
    api.add_resource(ResetPassword, "reset-password", "reset-password/<string:token>")


def create_app(env):
    app = Flask(__name__)

    app.config.from_object(app_config[env])
    app.register_blueprint(dbsetup)

    # declare the available routes
    create_routes(app)

    # allow cross-origin (CORS)
    CORS(app, origins=app.config["CORS_ORIGINS"])

    # set up authorization
    app.jwt = JWTManager(app)

    # initialize Mail
    app.mail = Mail(app)

    # check the user role in the JSON Web Token (JWT)
    @app.jwt.user_claims_loader
    def role_loader(identity):
        user = UserModel.find(identity)
        return {
            "email": user.email,
            "phone": user.phone,
            "firstName": user.firstName,
            "lastName": user.lastName,
            "role": user.role.value,
        }

    # checking if the token's jti (jwt id) is in the set of revoked tokens
    # this check is applied globally (to all routes that require jwt)
    @app.jwt.token_in_blacklist_loader
    def check_if_token_in_blacklist(decrypted_token):
        jti = decrypted_token["jti"]
        return RevokedTokensModel.is_jti_blacklisted(jti)

    # Format jwt "Missing authorization header" messages
    @app.jwt.unauthorized_loader
    def format_unauthorized_message(message):
        return {app.config["JWT_ERROR_MESSAGE_KEY"]: message.capitalize()}, 401

    db.init_app(app)
    ma.init_app(app)
    return app
