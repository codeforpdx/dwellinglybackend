import os
import logging
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_mailman import Mail
from models.user import UserModel
from models.revoked_tokens import RevokedTokensModel

from db import db
from ma import ma
from manage import dbsetup
from config.environment import app_environments
from config.routes import Routes


def create_app(env):
    app = Flask(__name__)

    app.config.from_object(app_environments[env])
    app.register_blueprint(dbsetup)

    # Define the available routes
    Routes.routing(app)

    # allow cross-origin (CORS)
    CORS(app, origins=app.config["CORS_ORIGINS"])

    # set up authorization
    app.jwt = JWTManager(app)

    # initialize Mail
    app.mail = Mail(app)

    # check the user role in the JSON Web Token (JWT)
    @app.jwt.additional_claims_loader
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
    @app.jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, decrypted_token):
        jti = decrypted_token["jti"]
        return RevokedTokensModel.is_jti_revoked(jti)

    # Format jwt "Missing authorization header" messages
    @app.jwt.unauthorized_loader
    def format_unauthorized_message(message):
        return {app.config["JWT_ERROR_MESSAGE_KEY"]: message.capitalize()}, 401

    if os.getenv("DB_LOGGING"):
        logging.basicConfig()
        logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)

    db.init_app(app)
    ma.init_app(app)
    return app
