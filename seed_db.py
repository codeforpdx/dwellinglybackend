from app import create_app
from db import db
from data.seedData import seedData

app = create_app()
with app.app_context():
    db.drop_all()
    db.create_all()
    seedData()
