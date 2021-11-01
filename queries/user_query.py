from sqlalchemy import column, false

from nobiru.nobiru_query import NobiruQuery


class UserQuery(NobiruQuery):
    def active(self):
        return self.where(column("archived") == false())

    def pending(self):
        return self.where(column("type") == "user")
