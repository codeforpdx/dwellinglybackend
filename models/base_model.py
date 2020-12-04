from flask import abort
from marshmallow import ValidationError, EXCLUDE
from db import db
from datetime import datetime


class BaseModel(db.Model):
    __abstract__ = True

    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow, default=datetime.utcnow, nullable=False)

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
    def create(cls, schema, payload):
        attrs = cls.validate(schema, payload)
        obj = cls(**attrs)
        obj.save_to_db()

        return obj

    @classmethod
    def update(cls, schema, id, payload):
        obj = cls.find(id)
        attrs = cls.validate(schema, payload, partial=True)

        for k, v in attrs.items():
            setattr(obj, k, v)

        obj.save_to_db()

        return obj

    @staticmethod
    def validate(schema, payload, partial=False):
        try:
            return schema().load(payload, unknown=EXCLUDE, partial=partial)
        except ValidationError as err:
            abort(400, err.messages)

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
