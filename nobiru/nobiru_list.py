from db import db
from flask import abort
from nobiru.nobiru import Nobiru
from sqlalchemy.orm.collections import InstrumentedList
from sqlalchemy.orm.collections import collection


class NobiruList(InstrumentedList):
    def json(self, **kwargs):
        return Nobiru.json(self, **kwargs)

    @collection.remover
    def delete(self, entity):
        try:
            self.remove(entity)
            db.session.commit()
        except ValueError:
            abort(404, f"{entity._name()} not found")

    def find(self, id):
        try:
            return next(x for x in self if x.id == id)

        except StopIteration:
            abort(404, "ID not found")
