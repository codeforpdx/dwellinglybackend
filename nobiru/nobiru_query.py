from nobiru.nobiru import Nobiru
from flask_sqlalchemy import BaseQuery


class NobiruQuery(BaseQuery):
    def json(self):
        return Nobiru.json(self)
