from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager, jwt_refresh_token_required, create_access_token, get_jwt_identity
from flask_cors import CORS
from resources.admin_required import admin_required
from models.user import UserModel
from models.property import PropertyModel
from models.revoked_tokens import RevokedTokensModel
from resources.user import UserRegister, User, UserLogin, ArchiveUser, UsersRole, UserAccessRefresh
from resources.property import Properties, Property, ArchiveProperty
from flask_mail import Mail
from resources.email import Email
import os
from db import db

app = Flask(__name__)
#config DataBase
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['JWT_AUTH_USERNAME_KEY'] = 'email'
# Enable blacklisting and specify what kind of tokens to check against the blacklist
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
app.secret_key = 'dwellingly' #Replace with Random Hash

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
app.config['MAIL_SUPPRESS_SEND'] = False #same as testing 
app.config['MAIL_ASCII_ATTACHMENTS'] = False

#allow cross-origin (CORS)
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = False
CORS(app)

api = Api(app)

db.init_app(app) #need to solve this 

@app.before_first_request
def create_tables():
    db.create_all()
    # seedData()

def seedData():
    user = UserModel(email="user1@dwellingly.org", role="admin", firstName="user1", lastName="tester", password="1234", archived=0)
    db.session.add(user)
    user = UserModel(email="user2@dwellingly.org", role="admin", firstName="user2", lastName="tester", password="1234", archived=0)
    db.session.add(user)
    user = UserModel(email="user3@dwellingly.org", role="admin", firstName="user3", lastName="tester", password="1234", archived=0)
    db.session.add(user)
    user = UserModel(email="MisterSir@dwellingly.org", role="property-manager", firstName="Mr.", lastName="Sir", password="1234", archived=0)
    db.session.add(user)
    user = UserModel(email="user3@dwellingly.org", role="property-manager", firstName="Gray", lastName="Pouponn", password="1234", archived=0)
    db.session.add(user)

    newProperty = PropertyModel(name="test1", address="123 NE FLanders St", city="Portland", state="OR", zipcode="97207", propertyManager=5, tenants=3, dateAdded="2020-04-12", archived=0)
    db.session.add(newProperty)
    newProperty = PropertyModel(name="Meerkat Manor", address="Privet Drive", city="Portland", state="OR", zipcode="97207", propertyManager=4, tenants=6, dateAdded="2020-04-12", archived=0)
    db.session.add(newProperty)
    newProperty = PropertyModel(name="The Reginald", address="Aristocrat Avenue", city="Portland", state="OR", zipcode="97207", propertyManager=5, tenants=4, dateAdded="2020-04-12", archived=0)
    db.session.add(newProperty)



    revokedToken = RevokedTokensModel(jti="855c5cb8-c871-4a61-b3d8-90249f979601")
    db.session.add(revokedToken)

    db.session.commit()

jwt = JWTManager(app) # /authorization 

mail = Mail(app) #init Mail


@jwt.user_claims_loader
#check if user role == admin
def role_loader(identity): #identity = user.id in JWT
    user = UserModel.find_by_id(identity)
    return {
        'email': user.email,
        'firstName': user.firstName,
        'lastName': user.lastName,
        'is_admin': (user.role == 'admin')
    }
    
# checking if the token's jti (jwt id) is in the set of revoked tokens
# this check is applied globally (to all routes that require jwt)
@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return RevokedTokensModel.is_jti_blacklisted(jti)


api.add_resource(UserRegister, '/register')
api.add_resource(Property,'/properties/<string:name>') #TODO change to ID
api.add_resource(Properties,'/properties')
api.add_resource(ArchiveProperty,'/properties/archive/<int:id>')
api.add_resource(User, '/user/<int:user_id>')
api.add_resource(UsersRole, '/users/role')
api.add_resource(ArchiveUser, '/user/archive/<int:user_id>')
api.add_resource(UserLogin, '/login')
api.add_resource(Email, '/user/message')
api.add_resource(UserAccessRefresh, '/refresh')


if __name__ == '__main__':
    db.init_app(app) 
    app.run(port=5000, debug=True)
