from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager, jwt_refresh_token_required, create_access_token, get_jwt_identity
from flask_cors import CORS
from flask_mail import Mail
from resources.admin_required import admin_required
from models.user import UserModel, RoleEnum
from models.property import PropertyModel
from models.tenant import TenantModel
from models.tenant_staff_link import StaffTenantLink
from models.revoked_tokens import RevokedTokensModel
from resources.user import UserRegister, User, UserLogin, ArchiveUser, UsersRole, UserAccessRefresh, UserRoles
from resources.reset_password import ResetPassword
from resources.property import Properties, Property, ArchiveProperty
from resources.tenants import Tenants
from resources.emergency_contacts import EmergencyContacts
from flask_mail import Mail
from resources.email import Email
from resources.tickets import Ticket, Tickets
from resources.lease import Lease, Leases
from resources.widgets import Widgets
import os
from db import db

def config_app(app):
    #config DataBase
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL", default = 'sqlite:///data.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['PROPAGATE_EXCEPTIONS'] = True
    app.secret_key = 'dwellingly' #Replace with Random Hash
    app.config['JWT_AUTH_USERNAME_KEY'] = 'email'

    # During development, it makes sense to allow permanent token validity
    # Replace these configs before production release.
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False
    app.config['JWT_REFRESH_TOKEN_EXPIRES'] = False

    # Enable blacklisting and specify what kind of tokens to check against the blacklist
    app.config['JWT_BLACKLIST_ENABLED'] = True
    app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']

    #configure mail server
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True
    app.config['MAIL_DEBUG'] = True #same as app
    app.config['MAIL_USERNAME'] = "dwellingly@gmail.com" #not active
    app.config['MAIL_PASSWORD'] = "1234567thisisnotreal"
    # app.config['MAIL_USERNAME'] = os.environ['EMAIL_USERNAME']
    # app.config['MAIL_PASSWORD'] = os.environ['EMAIL_PASSWORD']
    # app.config['MAIL_DEFAULT_SENDER'] = 'noreply@dwellingly.com'
    app.config['MAIL_MAX_EMAILS'] = 3
    app.config['MAIL_ASCII_ATTACHMENTS'] = False


def create_routes(app):
    api = Api(app, prefix="/api/")
    api.add_resource(UserRegister, 'register')
    api.add_resource(Property,'properties/<string:name>') #TODO change to ID
    api.add_resource(Properties,'properties')
    api.add_resource(ArchiveProperty,'properties/archive/<int:id>')
    api.add_resource(User, 'user')
    api.add_resource(User, 'user/<int:user_id>')
    api.add_resource(UsersRole, 'users/role')
    api.add_resource(ArchiveUser, 'user/archive/<int:user_id>')
    api.add_resource(UserLogin, 'login')
    api.add_resource(UserRoles, 'roles')
    api.add_resource(Widgets, 'widgets')
    api.add_resource(Email, 'user/message')
    api.add_resource(UserAccessRefresh, 'refresh')
    api.add_resource(Tenants, 'tenants', 'tenants/<int:tenant_id>')
    api.add_resource(EmergencyContacts, 'emergencycontacts', 'emergencycontacts/<int:id>')
    api.add_resource(Lease, 'lease/<int:id>')
    api.add_resource(Leases, 'lease')
    api.add_resource(Tickets, 'tickets')
    api.add_resource(Ticket, 'tickets/<int:id>')
    api.add_resource(ResetPassword, 'reset-password', 'reset-password/<string:token>')

def check_for_admins():
    errorMsg = (
        "\n\n=-=-=-=-=-=-=-=\n"
        "WARNING! Database unusable. Did you forget to create and seed your database? `python manage.py create`"
        "\n=-=-=-=-=-=-=-=\n\n"
    )
    assert (os.path.isfile('./data.db')), errorMsg
    try:
        admins = UserModel.find_by_role(RoleEnum.ADMIN)
    except:
        print(errorMsg)
    else:
        if(not len(admins)):
            print(errorMsg)


def create_app():
    app = Flask(__name__)

    #configure the flask settings
    config_app(app)

    #declare the available routes
    create_routes(app)

    #allow cross-origin (CORS)
    CORS(app)

    # set up authorization
    app.jwt = JWTManager(app)

    # initialize Mail
    app.mail = Mail(app)

    # ensure the database has been initialized (development only)
    @app.before_first_request
    def decorated_check_for_admins(): check_for_admins()

    # check the user role in the JSON Web Token (JWT)
    @app.jwt.user_claims_loader
    def role_loader(identity):
        user = UserModel.find_by_id(identity)
        return {'email': user.email, 'phone': user.phone, 'firstName': user.firstName, 'lastName': user.lastName, 'is_admin': (user.role == RoleEnum.ADMIN)}

    # checking if the token's jti (jwt id) is in the set of revoked tokens
    # this check is applied globally (to all routes that require jwt)
    @app.jwt.token_in_blacklist_loader
    def check_if_token_in_blacklist(decrypted_token):
        jti = decrypted_token['jti']
        return RevokedTokensModel.is_jti_blacklisted(jti)

    db.init_app(app)
    return app


app = create_app()


if __name__ == '__main__':
    app.run(port=5000, debug=True)
