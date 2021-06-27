from models.user import UserModel


class Admin(UserModel):
    __mapper_args__ = {"polymorphic_identity": "admin"}
