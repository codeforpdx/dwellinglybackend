from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from models.user import UserModel
from resources.user import UserRegister, User, UserLogin
from resources.property import Properties, Property
from db import db
from flask_mail import Mail
from resources.email import Email
import os

app = Flask(__name__)
#config DataBase
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.secret_key = 'dwellingly' #Replace with Random Hash

#configure mail server
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_DEBUG'] = True #same as app
app.config['MAIL_USERNAME'] = os.environ['EMAIL_USER']
app.config['MAIL_PASSWORD'] = os.environ['EMAIL_PASSWORD']
# app.config['MAIL_DEFAULT_SENDER'] = 'noreply@dwellingly.com'
app.config['MAIL_MAX_EMAILS'] = 3
app.config['MAIL_SUPPRESS_SEND'] = False #same as testing 
app.config['MAIL_ASCII_ATTACHMENTS'] = False

#allow cross-origin (CORS)
CORS(app)

api = Api(app)

db.init_app(app) #need to solve this 

@app.before_first_request
def create_tables():
    db.create_all()

jwt = JWTManager(app) # /authorization 

mail = Mail(app) #init Mail

@jwt.user_claims_loader
#check if user role == admin
def role_loader(identity): #idenity = user.id in JWT
    user = UserModel.find_by_id(identity)
    if user.role == 'admin':
        return{'is_admin': True}
    return {'is_admin': False}
    

api.add_resource(UserRegister, '/register')
api.add_resource(Property,'/properties/<string:name>') #TODO change to ID
api.add_resource(Properties,'/properties')
api.add_resource(User, '/user/<int:user_id>')
api.add_resource(UserLogin, '/login')
api.add_resource(Email, '/user/message')


if __name__ == '__main__':
    # db.init_app(app) 
    app.run(port=5000, debug=True)