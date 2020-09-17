from datetime import datetime, timedelta
import time
import jwt
from db import db
from enum import Enum
from models.base_model import BaseModel
from flask import current_app
from jwt import ExpiredSignatureError


class RoleEnum(Enum):
    PENDING = 0
    TENANT = 1
    PROPERTY_MANAGER = 2
    STAFF = 3
    ADMIN = 4


class UserModel(BaseModel):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100))
    role = db.Column(db.Enum(RoleEnum), default=RoleEnum.PENDING)
    firstName = db.Column(db.String(80))
    lastName = db.Column(db.String(80))
    fullName = db.column_property(firstName + ' ' + lastName)
    phone = db.Column(db.String(25))
    password = db.Column(db.String(128))
    archived = db.Column(db.Boolean)
    lastActive = db.Column(db.DateTime, default=datetime.utcnow)
    created = db.Column(db.DateTime, default=datetime.utcnow)


    def __init__(self, firstName, lastName, email, password, phone, role, archived):
        self.firstName = firstName
        self.lastName = lastName
        self.email = email
        self.phone = phone
        self.password = password
        self.role = role
        self.archived = False
        self.lastActive = datetime.utcnow()
        self.created = datetime.utcnow()

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

    def json(self):
        return {
            'id': self.id,
            'firstName': self.firstName,
            'lastName': self.lastName,
            'email': self.email,
            'phone': self.phone,
            'role': self.role.value,
            'created': self.created.strftime('%Y-%m-%d %H:%M:%S %Z'),
            'archived': self.archived,
            'lastActive': self.lastActive.strftime('%Y-%m-%d %H:%M:%S %Z')
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
        dateTime = datetime.now() - timedelta(days = days)
        return db.session.query(UserModel).filter(UserModel.role == role).order_by(UserModel.created.desc()).limit(3).all()
      
    @classmethod
    def find_by_role_and_name(cls, role, name):
        likeName = f'%{name}%'
        return cls.query.filter((UserModel.role == role) & (UserModel.firstName.ilike(likeName) | UserModel.lastName.ilike(likeName))).all()

    def full_name(self):
        return '{} {}'.format(self.firstName, self.lastName)