import os
from db import db
from models.user import UserModel, OAuthModel
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_claims, get_raw_jwt, get_jwt_identity, jwt_refresh_token_required
from flask_dance.contrib.google import google, make_google_blueprint
from flask_dance.consumer import oauth_authorized
from flask_dance.consumer.storage.sqla import SQLAlchemyStorage
from flask import redirect, Response

# Uses a flask 'app' to initialize the google oauth system
def init_google_oauth(app):
    google_blueprint = make_google_blueprint(
        scope=["profile", "email"],
        client_id=os.getenv("GOOGLE_OAUTH_CLIENT_ID"),
        client_secret=os.getenv("GOOGLE_OAUTH_CLIENT_SECRET"),
        storage=SQLAlchemyStorage(OAuthModel, db.session, None),
        redirect_url="http://localhost:3000"
    )

    # Whenever a user sends a get request to /api/login/google
    # The user will be redirected to the google oauth page per the blueprint above
    app.register_blueprint(google_blueprint, url_prefix="/api/login")

    # @app.route("/api/login/google/success")
    # def googleAuthRedirect():
    #     #At this point, there should be a google login for the given user

    # After authorization from google.
    @oauth_authorized.connect_via(google_blueprint)
    def google_logged_in(blueprint, token):
        if not token:
            print("Google Login Failed")
            return False
        response = blueprint.session.get("/oauth2/v1/userinfo")
        if not response.ok or not response.json:
            print("Failed to fetch user from Google")
            return False
        googleData = response.json()

        # Look for info from google
        print("Looking for existing oauth login")
        oauth = OAuthModel.query.filter_by(
            provider=blueprint.name,
            provider_user_id=googleData['id']
        ).first()

        if oauth:
            print('found')
        else:
            print("not found. creating new oauth entry")
            oauth = OAuthModel(
                provider=blueprint.name,
                provider_user_id=googleData['id'],
                token=token
            )

        print('checking if oauth is linked to an account')
        if oauth.user:
            print("This google account is already linked to a dwellingly account")
            print("Logging the user in...")

        else:
            print("No account linked")
            print("Checking if dwellingly account exists with this email..")
            user = UserModel.find_by_email(googleData['email'])
            if user:
                print("Dwellingly account already exists with this email")
                print("Linking the oauth account to the existing account ")
            else:
                print("No account exists with this email")
                print("Creating and linking new account")
                user = UserModel(
                    firstName=googleData['given_name'],
                    lastName=googleData['family_name'],
                    email=googleData['email'],
                )
                user.save_to_db()
            oauth.user = user
            oauth.save_to_db()

        access_token = create_access_token(identity=oauth.user.id, fresh=True) 
        # refresh_token = create_refresh_token(user.id)
        headers = {"Authorization": f"Bearer {access_token}", "Location": "http://localhost:3000"}

        res = Response(status=302, headers=headers)

        return res