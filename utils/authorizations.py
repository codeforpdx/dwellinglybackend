from flask_jwt_extended import jwt_required, get_jwt_claims
from models.user import RoleEnum

not_authorized_msg = {"message": "Not Authorized"}, 401


def admin_required(func):
    @jwt_required
    def check_admin_wrapper(*args, **kwargs):
        if admin():
            return func(*args, **kwargs)
        else:
            return not_authorized_msg

    return check_admin_wrapper


def staff_level_required(func):
    @jwt_required
    def check_staff_level(*args, **kwargs):
        if _staff_level():
            return func(*args, **kwargs)
        else:
            return not_authorized_msg

    return check_staff_level


def pm_level_required(func):
    @jwt_required
    def check_pm_level(*args, **kwargs):
        if _pm_level():
            return func(*args, **kwargs)
        else:
            return not_authorized_msg

    return check_pm_level


def admin():
    return get_jwt_claims()["role"] == RoleEnum.ADMIN.value


def staff():
    return get_jwt_claims()["role"] == RoleEnum.STAFF.value


def pm():
    return get_jwt_claims()["role"] == RoleEnum.PROPERTY_MANAGER.value


def _staff_level():
    return staff() or admin()


def _pm_level():
    return pm() or _staff_level()
