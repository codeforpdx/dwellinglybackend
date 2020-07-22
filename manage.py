from app import create_app
from flask_script import Manager, prompt_bool
from db import db
from data.seedData import seedData

app = create_app()
manager = Manager(app)

"""
    *****Database Commands*****
"""

@manager.command
def populate():
    """Seed the database with default data"""
    seedData()

@manager.command
def create():
    """Creates database tables and populates with seed data"""
    db.create_all()
    populate()

@manager.command
def drop():
    """Drops all database tables"""
    if prompt_bool("Are you sure you want to lose all your data"):
        db.drop_all()

@manager.command
def recreate():
    """Recreates database table and populates with seed data. Know that this will reset your db to defaults"""
    drop()
    create()


if __name__ == "__main__":
    manager.run()
