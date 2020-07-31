from db import db
from flask_dance.consumer.storage.sqla import OAuthConsumerMixin

class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100))
    role = db.Column(db.String(20))
    firstName = db.Column(db.String(80))
    lastName = db.Column(db.String(80))
    fullName = db.column_property(firstName + ' ' + lastName)
    password = db.Column(db.String(80))
    archived = db.Column(db.Boolean)

    def __init__(self, firstName, lastName, email, password=None, role='pending', archived=False):
        self.firstName = firstName
        self.lastName = lastName
        self.email = email
        self.password = password
        self.role = role if role else 'pending'
        self.archived = archived if archived else False

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
    
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def json(self): 
        return {
            'id': self.id,
            'firstName': self.firstName,
            'lastName': self.lastName,
            'email': self.email,
            'role': self.role,
            'archived': self.archived
        }

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_role(cls, role):
        return cls.query.filter_by(role=role).all()


# A table with columns for provider (i.e. google), provider_user_id, token, and a user relationship
# Used by flask-dance for tracking oauth accounts
class OAuthModel(OAuthConsumerMixin, db.Model):
    provider_user_id = db.Column(db.String(40))
    user_id = db.Column(db.Integer, db.ForeignKey(UserModel.id, ondelete="CASCADE"))
    user = db.relationship(UserModel, backref=db.backref("oauth_connections", cascade="all, delete"))

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()