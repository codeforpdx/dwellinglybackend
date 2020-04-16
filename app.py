from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from models.user import UserModel
from models.property import PropertyModel
from models.revoked_tokens import RevokedTokensModel
from resources.user import UserRegister, User, UserLogin, ArchiveUser, UsersRole
from resources.property import Properties, Property, ArchiveProperty
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
api.add_resource(Property,'/properties/<string:name>')
api.add_resource(Properties,'/properties')
api.add_resource(ArchiveProperty,'/properties/archive/<int:id>')
api.add_resource(User, '/user/<int:user_id>')
api.add_resource(UsersRole, '/users/role')
api.add_resource(ArchiveUser, '/user/archive/<int:user_id>')
api.add_resource(UserLogin, '/login')


if __name__ == '__main__':
    # db.init_app(app) 
    app.run(port=5000, debug=True)