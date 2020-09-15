from flask_jwt_extended import jwt_required, get_jwt_claims
from models.user import UserModel, RoleEnum

def dev_required(func):
    @jwt_required
    def check_dev_wrapper(*args, **kwargs):
        #check if user is dev, if not return 401
        claims = get_jwt_claims() 
        user = UserModel.find_by_email(claims['email'])
        if user.role != RoleEnum.DEV:
            return {'message': "Dev Access Required"}, 401

        return func(*args, **kwargs)

    return check_dev_wrapper

