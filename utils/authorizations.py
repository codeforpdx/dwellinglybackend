from flask_jwt_extended import jwt_required, get_jwt_claims

def admin_required(func):
    @jwt_required
    def check_admin_wrapper(*args, **kwargs):
        if admin():
            return func(*args, **kwargs)
        else:
            return {'message': 'Not Authorized'}, 401

    return check_admin_wrapper

def admin():
    return get_jwt_claims()['is_admin']
