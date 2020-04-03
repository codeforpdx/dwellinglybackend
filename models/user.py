from db import db


class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100))
    role = db.Column(db.String(20))
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))
    archived = db.Column(db.Boolean)

    def __init__(self, username, password, email, role, archived):
        self.username = username
        self.password = password
        self.email = email
        self.role = role
        self.archived = False

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
    
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def json(self): 
        print('DBG: Userid: '+ str(self.id))
        print('DBG: UserName: '+ self.username)
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'role': self.role,
            'archived': self.archived
        }

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_role(cls, role):
        return cls.query.filter_by(role=role).all()