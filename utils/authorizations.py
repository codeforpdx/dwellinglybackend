from flask_jwt_extended import jwt_required, current_user

not_authorized_msg = {"message": "Not Authorized"}, 401


def admin_required(func):
    @jwt_required()
    def check_admin_wrapper(*args, **kwargs):
        if current_user.is_admin():
            return func(*args, **kwargs)
        else:
            return not_authorized_msg

    return check_admin_wrapper


def staff_level_required(func):
    @jwt_required()
    def check_staff_level(*args, **kwargs):
        if current_user.has_staff_privs():
            return func(*args, **kwargs)
        else:
            return not_authorized_msg

    return check_staff_level


def pm_level_required(func):
    @jwt_required()
    def check_pm_level(*args, **kwargs):
        if current_user.has_pm_privs():
            return func(*args, **kwargs)
        else:
            return not_authorized_msg

    return check_pm_level
