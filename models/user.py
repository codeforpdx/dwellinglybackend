from flask import current_app
from datetime import datetime, timedelta
import bcrypt
import time
import jwt
from db import db
from enum import Enum
from models.base_model import BaseModel
from flask import current_app
from jwt import ExpiredSignatureError
from utils.time import Time


class RoleEnum(Enum):
    PENDING = 0
    TENANT = 1
    PROPERTY_MANAGER = 2
    STAFF = 3
    ADMIN = 4


class UserModel(BaseModel):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    role = db.Column(db.Enum(RoleEnum), default=RoleEnum.PENDING)
    firstName = db.Column(db.String(80))
    lastName = db.Column(db.String(80))
    fullName = db.column_property(firstName + ' ' + lastName)
    phone = db.Column(db.String(25))
    hash_digest = db.Column(db.LargeBinary(60))
    archived = db.Column(db.Boolean)
    lastActive = db.Column(db.DateTime, default=datetime.utcnow)


    def __init__(self, **kwargs):
        super(UserModel, self).__init__(**kwargs)
        self.hash_digest = UserModel.hash_pw(kwargs['password'])
        self._password = None
        self.archived = False

    @property
    def password(self):
        return self.hash_digest

    @password.setter
    def password(self, new_password):
        self._password = UserModel.hash_pw(new_password)

    def update_last_active(self):
        self.lastActive = datetime.utcnow()
        db.session.commit()

    def reset_password_token(self):
        ten_minutes = 600
        return jwt.encode(
                {'user_id': self.id, 'exp': time.time() + ten_minutes},
                current_app.secret_key,
                algorithm='HS256'
            ).decode('utf-8')

    @staticmethod
    def validate_reset_password(token):
        try:
            token = jwt.decode(token, current_app.secret_key, algorithms=['HS256'])
            return UserModel.find_by_id(token['user_id'])
        except ExpiredSignatureError:
            return None

    @staticmethod
    def hash_pw(plaintext_password):
        return bcrypt.hashpw(bytes(plaintext_password, 'utf-8'), bcrypt.gensalt(current_app.config['WORK_FACTOR']))

    def check_pw(self, plaintext_password):
        return bcrypt.checkpw(bytes(plaintext_password, 'utf-8'), self.hash_digest)

    def json(self):
        return {
            'id': self.id,
            'firstName': self.firstName,
            'lastName': self.lastName,
            'email': self.email,
            'phone': self.phone,
            'role': self.role.value,
            'archived': self.archived,
            'lastActive': Time.format_date(self.lastActive),
            'created_at': Time.format_date(self.created_at),
            'updated_at': Time.format_date(self.updated_at)
        }

    def widgetJson(self, propertyName, date):
        return{
            'id': self.id,
            'stat': date,
            'desc': "{} {}".format(self.firstName, self.lastName),
            'subtext': propertyName
        }

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_by_role(cls, role):
        return cls.query.filter_by(role=role).all()

    @classmethod
    def find_recent_role(cls, role, days):
        dateTime = datetime.utcnow() - timedelta(days = days)
        return db.session.query(UserModel).filter(UserModel.role == role).order_by(UserModel.created_at.desc()).limit(3).all()

    @classmethod
    def find_by_role_and_name(cls, role, name):
        likeName = f'%{name}%'
        return cls.query.filter((UserModel.role == role) & (UserModel.firstName.ilike(likeName) | UserModel.lastName.ilike(likeName))).all()

    def full_name(self):
        return '{} {}'.format(self.firstName, self.lastName)

    def save_to_db(self):
        if self._password:
            self.hash_digest = self._password
        db.session.add(self)
        db.session.commit()
        self._password = None

