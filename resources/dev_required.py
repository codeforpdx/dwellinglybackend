from flask_jwt_extended import jwt_required, get_jwt_claims

def dev_required(func):
    @jwt_required
    def check_dev_wrapper(*args, **kwargs):
        #check if is_dev exist. If not discontinue function
        claims = get_jwt_claims() 
        print(get_jwt_claims())
        if not claims['is_dev']:
            return {'message': "Dev Access Required"}, 401

        return func(*args, **kwargs)

    return check_dev_wrapper

