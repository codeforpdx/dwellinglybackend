from flask_restful import Resource, reqparse
from enum import Enum
from resources.admin_required import admin_required
from models.user import UserModel
from models.revoked_tokens import RevokedTokensModel
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_claims, get_raw_jwt, get_jwt_identity, jwt_refresh_token_required


class RoleEnum(Enum):
    PENDING = 0
    TENANT = 1
    PROPERTYMANAGER = 2
    STAFF = 3
    ADMIN = 4

class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('firstName',type=str,required=True,help="This field cannot be blank.")
    parser.add_argument('lastName',type=str,required=True,help="This field cannot be blank.")
    parser.add_argument('email',type=str,required=True,help="This field cannot be blank.")
    parser.add_argument('password', type=str, required=True, help="This field cannot be blank.")
    parser.add_argument('role',type=int,required=False,help="This field is not required.")
    parser.add_argument('archived',type=str,required=False,help="This field is not required.")
    
    def post(self):
        data = UserRegister.parser.parse_args()

        if UserModel.find_by_email(data['email']):
            return {"message": "A user with that email already exists"}, 400

        user = UserModel(data['firstName'], data['lastName'], data['email'], data['password'], data['role'], data['archived'])
        user.save_to_db()

        return {"message": "User created successfully."}, 201

class User(Resource):
    @admin_required
    def get(self, user_id):
        user = UserModel.find_by_id(user_id)

        if not user:
            return {'message': 'User Not Found'}, 404

        # hard coded return as .json() is not compatiable with user model and sqlalchemy
        return {
            'id': str(user.id),
            'firstName': user.firstName,
            'lastName': user.lastName,
            'email': user.email,
            'role': user.role,
            'archived': user.archived
        }, 200
        
    @admin_required
    def patch(self,user_id):
        parser = reqparse.RequestParser()
        parser.add_argument('role',type=str,required=True,help="This field cannot be blank.")

        user = UserModel.find_by_id(user_id)
        if not user:
            return {"Message": "Unable to update user"}, 400

        data = parser.parse_args()
        user.role = data['role']
        try:
            user.save_to_db()
        except:
            return {'Message': 'An Error Has Occurred'}, 500

        return user.json(), 201

    @admin_required
    def delete(self, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"Message": "Unable to delete User"}, 400
        user.delete_from_db()
        return {"Message": "User deleted"}, 200

class ArchiveUser(Resource):

    @admin_required
    def post(self, user_id):
        user = UserModel.find_by_id(user_id)
        if(not user):
            return{'Message': 'User cannot be archived'}, 400

        user.archived = not user.archived
        try:
            user.save_to_db()
        except:
            return {'Message': 'An Error Has Occured'}, 500

        if user.archived:
            # invalidate access token
            jti = get_raw_jwt()['jti']
            revokedToken = RevokedTokensModel(jti=jti)
            revokedToken.save_to_db()

        return user.json(), 201

class UserLogin(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('email',type=str,required=True,help="This field cannot be blank.")
    parser.add_argument('password', type=str, required=True, help="This field cannot be blank.")

    def post(self):
        data = UserLogin.parser.parse_args()

        user = UserModel.find_by_email(data['email'])

        if user and user.archived:
            return {"message": "Not a valid user"}, 403

        if user and safe_str_cmp(user.password, data['password']):
            access_token = create_access_token(identity=user.id, fresh=True) 
            refresh_token = create_refresh_token(user.id)
            return {
                'access_token': access_token,
                'refresh_token': refresh_token
            }, 200

        return {"message": "Invalid Credentials!"}, 401       

class UsersRole(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('userrole',type=str,required=True,help="This field cannot be blank.")

    @admin_required
    def post(self):
        data = UsersRole.parser.parse_args()
        users = UserModel.find_by_role(data['userrole'])
        return {'users': [user.json() for user in users]}

# This endpoint allows the app to use a refresh token to get a new access token 
class UserAccessRefresh(Resource):
    
    # The jwt_refresh_token_required decorator insures a valid refresh
    # token is present in the request before calling this endpoint. We
    # can use the get_jwt_identity() function to get the identity of
    # the refresh token, and use the create_access_token() function again
    # to make a new access token for this identity.
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        ret = {
            'access_token': create_access_token(identity=current_user)
        }
        return ret, 200
