from flask_jwt_extended import jwt_required, get_jwt_claims

def admin_required(func):
    @jwt_required
    def check_admin_wrapper(*args, **kwargs):
        #check if is_admin exist. If not discontinue function
        claims = get_jwt_claims() 
        if not claims['is_admin']:
            return {'message': "Admin Access Required"}, 401

        return func(*args, **kwargs)

    return check_admin_wrapper

