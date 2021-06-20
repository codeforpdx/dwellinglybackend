from flask import current_app
from nobiru.nobiru_list import NobiruList
from datetime import datetime
from models.tickets import TicketModel
import bcrypt
import time
import jwt
from db import db
from enum import Enum
from models.base_model import BaseModel
import models.notes
from jwt import ExpiredSignatureError
from utils.time import Time
from sqlalchemy import and_


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


class UserModel(BaseModel):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    role = db.Column(db.Enum(RoleEnum), default=None)
    firstName = db.Column(db.String(100), nullable=False)
    lastName = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    # hash_digest = db.Column(db.LargeBinary(60))
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
        return self._password

    @password.setter
    def password(self, plaintext_password):
        self._password = bcrypt.hashpw(
            plaintext_password.encode("utf-8"),
            bcrypt.gensalt(current_app.config["WORK_FACTOR"]),
        )

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
        return bcrypt.checkpw(bytes(plaintext_password, "utf-8"), self.password)

    def json(self):
        return {
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

    def widgetJson(self, propertyName, date):
        return {
            "id": self.id,
            "stat": date,
            "desc": "{} {}".format(self.firstName, self.lastName),
            "subtext": propertyName,
        }

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_by_role(cls, role):
        return cls.query.filter_by(role=role).all()

    @classmethod
    def find_recent_role(cls, role, days):
        return (
            db.session.query(UserModel)
            .filter(UserModel.role == role)
            .order_by(UserModel.created_at.desc())
            .limit(3)
            .all()
        )

    @classmethod
    def find_by_role_and_name(cls, role, name):
        likeName = f"%{name}%"
        return cls.query.filter(
            (UserModel.role == role)
            & (UserModel.firstName.ilike(likeName) | UserModel.lastName.ilike(likeName))
        ).all()

    @classmethod
    def find_users_without_assigned_role(cls):
        return cls.query.filter(and_(cls.role.is_(None), cls.archived.is_(False)))

    def full_name(self):
        return "{} {}".format(self.firstName, self.lastName)
