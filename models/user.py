from flask import current_app
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
)
import bcrypt
import time
import jwt
from jwt import ExpiredSignatureError
from enum import Enum
from datetime import datetime

from db import db
from nobiru.nobiru_list import NobiruList
from queries.user_query import UserQuery
from models.tickets import TicketModel
from models.base_model import BaseModel
import models.notes
from utils.time import Time


class RoleEnum(Enum):
    PROPERTY_MANAGER = 2
    STAFF = 3
    ADMIN = 4

    @classmethod
    def get_values(cls):
        return [member.value for name, member in cls.__members__.items()]

    @classmethod
    def has_role(cls, role):
        role_values = cls.get_values()
        return role in role_values


class UserType(Enum):
    ADMIN = "admin"
    STAFF = "staff"
    PROPERTY_MANAGER = "property_manager"

    @classmethod
    def get(cls, value, default=None):
        return cls._values().get(value, default)

    @classmethod
    def _values(cls):
        return {member.value: member.value for member in cls.__members__.values()}


class UserModel(BaseModel):
    __tablename__ = "users"

    __mapper_args__ = {"polymorphic_identity": "user", "polymorphic_on": "type"}

    query_class = UserQuery

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    role = db.Column(db.Enum(RoleEnum), default=None)
    firstName = db.Column(db.String(100), nullable=False)
    lastName = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(40), nullable=False)
    _password = db.Column("password", db.LargeBinary(60))
    archived = db.Column(db.Boolean, default=False, nullable=False)
    lastActive = db.Column(db.DateTime, default=datetime.utcnow)

    notes = db.relationship(
        models.notes.NotesModel,
        backref=db.backref("user", lazy=True),
        collection_class=NobiruList,
    )

    authored_tickets = db.relationship(
        "TicketModel",
        backref="author",
        primaryjoin=id == TicketModel.author_id,
        collection_class=NobiruList,
    )

    @property
    def password(self):
        raise AttributeError("password field is not allowed to access")

    @password.setter
    def password(self, plaintext_password):
        self._password = bcrypt.hashpw(
            plaintext_password.encode("utf-8"),
            bcrypt.gensalt(current_app.config["WORK_FACTOR"]),
        )

    def validation_context(self):
        return {"email": self.email}

    def update_last_active(self):
        self.lastActive = datetime.utcnow()
        db.session.commit()

    def reset_password_token(self):
        ten_minutes = 600
        return jwt.encode(
            {"user_id": self.id, "exp": time.time() + ten_minutes},
            current_app.secret_key,
            algorithm="HS256",
        )

    @staticmethod
    def validate_reset_password(token):
        try:
            token = jwt.decode(token, current_app.secret_key, algorithms=["HS256"])
            return UserModel.find(token["user_id"])
        except ExpiredSignatureError:
            return None

    def check_pw(self, plaintext_password):
        return bcrypt.checkpw(plaintext_password.encode("utf-8"), self._password)

    def json(self, refresh_token=False):
        base_json = {
            "id": self.id,
            "firstName": self.firstName,
            "lastName": self.lastName,
            "email": self.email,
            "phone": self.phone,
            "role": self.role.value if self.role else None,
            "archived": self.archived,
            "lastActive": Time.format_date(self.lastActive),
            "created_at": Time.format_date(self.created_at),
            "updated_at": Time.format_date(self.updated_at),
        }
        return {**base_json, **self.serialize(), **self._make_token(refresh_token)}

    def serialize(self):
        return {}

    @staticmethod
    def authenticate(user, password):
        if user and (user.archived or user.type == "user" or user.role is None):
            return {"message": "Invalid user"}, 403
        elif user and user.check_pw(password):
            access_token = create_access_token(identity=user, fresh=True)
            refresh_token = create_refresh_token(user)
            user.update_last_active()
            return {"access_token": access_token, "refresh_token": refresh_token}, 200
        else:
            return {"message": "Invalid credentials"}, 401

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def take(cls, num):
        return cls.query.order_by(cls.created_at.desc()).limit(num).all()

    @classmethod
    def find_by_role_and_name(cls, role, name):
        likeName = f"%{name}%"
        return cls.query.filter(
            (UserModel.role == role)
            & (UserModel.firstName.ilike(likeName) | UserModel.lastName.ilike(likeName))
        ).all()

    def full_name(self):
        return "{} {}".format(self.firstName, self.lastName)

    def is_admin(self):
        return False

    def has_staff_privs(self):
        return False

    def has_pm_privs(self):
        return False

    def _make_token(self, refresh):
        if refresh:
            return {
                "access_token": create_access_token(identity=self, fresh=True),
                "refresh_token": create_refresh_token(self),
            }
        else:
            return {}
