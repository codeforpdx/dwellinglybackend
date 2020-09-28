from db import db


class BaseModel(db.Model):
    __abstract__ = True

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

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def json(self):
        raise NotImplementedError(f"This {self.__class__} must implement a <json> method")

    def __repr__(self):
        return f'<{type(self).__name__} {self.json()}>'

    @classmethod
    def _name(cls):
        return cls.__name__.replace('Model', '')
