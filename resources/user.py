from flask_restful import Resource, reqparse
from models.user import UserModel
from models.revoked_tokens import RevokedTokensModel
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_claims, get_raw_jwt


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('firstName',type=str,required=True,help="This field cannot be blank.")
    parser.add_argument('lastName',type=str,required=True,help="This field cannot be blank.")
    parser.add_argument('email',type=str,required=True,help="This field cannot be blank.")
    parser.add_argument('password', type=str, required=True, help="This field cannot be blank.")
    parser.add_argument('role',type=str,required=True,help="This field cannot be blank.")
    parser.add_argument('archived',type=str,required=False,help="This field is not required.")
    
    def post(self):
        data = UserRegister.parser.parse_args()

        if UserModel.find_by_email(data['email']):
            return {"message": "A user with that email already exists"}, 400

        user = UserModel(data['firstName'], data['lastName'], data['email'], data['password'], data['role'], data['archived'])
        user.save_to_db()

        return {"message": "User created successfully."}, 201

class User(Resource):

    @jwt_required
    def get(self, user_id):
        #check if is_admin exist if not discontinue function
        claims = get_jwt_claims()         
        if not claims['is_admin']:
            return {'Message', "Admin Access Required"}, 401

        user = UserModel.find_by_id(user_id)

        if not user:
            return {'message': 'User Not Found'}, 404

        # hard coded return as .json() is not compatiable with user model and sqlalchemy
        return {
            'id': str(user.id),
            'username': user.username,
            'email': user.email,
            'role': user.role,
            'archived': user.archived
        }, 200
        

    @jwt_required
    def delete(self, user_id):
        #check if is_admin exists - if not discontinue function
        claims = get_jwt_claims()         
        if not claims['is_admin']:
            return {'Message', "Admin Access Required"}, 401

        user = UserModel.find_by_id(user_id)
        if not user:
            return {"Message", "Unable to delete User"}, 404 
        user.delete_from_db()
        return {"Message": "User deleted"}, 200

#pull all users - for debugging purposes disable before production
class Users(Resource):
    @jwt_required
    def get(self):
        #check if is_admin exists - if not discontinue function
        claims = get_jwt_claims() 
        if not claims['is_admin']:
            return {'Message', "Admin Access Required"}, 401
        return {'Users': [user.json() for user in UserModel.query.all()]}

class ArchiveUser(Resource):

    @jwt_required
    def post(self, user_id):
        #check if is_admin exist if not discontinue function
        claims = get_jwt_claims() 

        if not claims['is_admin']:
            return {'Message', "Admin Access Required"}, 401

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

    @jwt_required
    def post(self):
        #check if is_admin exist if not discontinue function
        claims = get_jwt_claims() 
        if not claims['is_admin']:
            return {'Message', "Admin Access Required"}, 401

        data = UsersRole.parser.parse_args()
        users = UserModel.find_by_role(data['userrole'])
        return {'users': [user.json() for user in users]}
