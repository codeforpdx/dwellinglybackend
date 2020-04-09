from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager, jwt_refresh_token_required, create_access_token, get_jwt_identity
from flask_cors import CORS
from models.user import UserModel
from models.revoked_tokens import RevokedTokensModel
from resources.user import UserRegister, User, UserLogin, ArchiveUser, UsersRole, UserAccessRefresh
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
CORS(app)

api = Api(app)

db.init_app(app) #need to solve this 

@app.before_first_request
def create_tables():
    db.create_all()

jwt = JWTManager(app) # /authorization 

@jwt.user_claims_loader
#check if user role == admin
def role_loader(identity): #idenity = user.id in JWT
    user = UserModel.find_by_id(identity)
    if user.role == 'admin':
        return{'is_admin': True}
    return {'is_admin': False}
    
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
api.add_resource(UserAccessRefresh, '/refresh')

if __name__ == '__main__':
    # db.init_app(app) 
    app.run(port=5000, debug=True)