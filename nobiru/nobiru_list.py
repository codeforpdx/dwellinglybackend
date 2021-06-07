from db import db
from flask import abort
from nobiru.nobiru import Nobiru
from sqlalchemy.orm.collections import InstrumentedList
from sqlalchemy.orm.collections import collection


class NobiruList(InstrumentedList):
    def json(self):
        return Nobiru.json(self)

    @collection.remover
    def delete(self, entity):
        try:
            self.remove(entity)
            db.session.commit()
        except ValueError:
            abort(404, f"{entity._name()} not found")
