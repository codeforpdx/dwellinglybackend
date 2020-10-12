from flask import abort
from marshmallow import ValidationError, EXCLUDE
from db import db
from datetime import datetime


class BaseModel(db.Model):
    __abstract__ = True

    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find(cls, id):
        return cls.query.get_or_404(id, f'{cls._name()} not found')

    @classmethod
    def delete(cls, id):
        obj = cls.find(id)
        db.session.delete(obj)
        db.session.commit()

    @classmethod
    def create(cls, schema, attributes):
        try:
            attrs = schema().load(attributes, unknown=EXCLUDE)
        except ValidationError as err:
            abort(400, err.messages)

        obj = cls(**attrs)
        db.session.add(obj)
        db.session.commit()

        return obj

    @classmethod
    def update(cls, schema, id, attributes):
        obj = cls.find(id)
        try:
            attrs = schema().load(attributes, unknown=EXCLUDE, partial=True)
        except ValidationError as err:
            abort(400, err.messages)

        for k, v in attrs.items():
            setattr(obj, k, v)

        db.session.add(obj)
        db.session.commit()

        return obj

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return "<{!r} {!r}>".format(type(self).__name__, self.__dict__)

    @classmethod
    def _name(cls):
        return cls.__name__.replace('Model', '')
