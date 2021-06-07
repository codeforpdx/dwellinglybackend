from flask_sqlalchemy import SQLAlchemy
from nobiru.nobiru_query import NobiruQuery

db = SQLAlchemy(query_class=NobiruQuery)
