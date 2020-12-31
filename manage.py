import click
from db import db
from data.seedData import seedData
from flask import Blueprint

dbsetup = Blueprint("db", __name__)

"""
    *****Database Commands*****
"""


@dbsetup.cli.command("populate")
def populate():
    """Seed the database with default data"""
    seedData()


@dbsetup.cli.command("create")
def create():
    """Creates database tables and populates with seed data"""
    db.create_all()
    seedData()


@dbsetup.cli.command("drop")
def drop():
    """Drops all database tables"""
    if click.confirm("Are you sure you want to lose all your data"):
        db.drop_all()


@dbsetup.cli.command("recreate")
def recreate():
    """
    Recreates database table and populates with seed data.
    Know that this will reset your db to defaults
    """
    if click.confirm("Are you sure you want to lose all your data"):
        db.drop_all()
        db.create_all()
        seedData()


if __name__ == "__main__":
    import sys

    print(
        "'pipenv run python manage.py {}' ".format(sys.argv[1])
        + "has been deprecated\n"
        + "please use 'pipenv run flask db {}'".format(sys.argv[1])
    )
