from nobiru.nobiru import Nobiru
from flask_sqlalchemy import BaseQuery
from sqlalchemy import column

from utils.time import TimeStamp


class NobiruQuery(BaseQuery):
    def json(self):
        return Nobiru.json(self)

    def updated_within(self, days=None):
        return self.filter(column("updated_at") >= TimeStamp.days_ago(days))
