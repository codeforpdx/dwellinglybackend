from models.user import UserModel


class Admin(UserModel):
    __mapper_args__ = {"polymorphic_identity": "admin"}

    def is_admin(self):
        return True

    def has_staff_privs(self):
        return True

    def has_pm_privs(self):
        return True
