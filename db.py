from flask_sqlalchemy import SQLAlchemy
from utils.nobiru import NobiruQuery

db = SQLAlchemy(query_class=NobiruQuery)
