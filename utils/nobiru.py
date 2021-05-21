from flask_sqlalchemy import BaseQuery
from sqlalchemy.orm.collections import InstrumentedList


class Nobiru:
    @staticmethod
    def json(collection):
        return [object.json() for object in collection]


class NobiruList(InstrumentedList):
    def json(self):
        return Nobiru.json(self)


class NobiruQuery(BaseQuery):
    def json(self):
        return Nobiru.json(self)
