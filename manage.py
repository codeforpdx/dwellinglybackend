import click

from db import db
from flask import Blueprint

dbsetup = Blueprint("db", __name__)

"""
    *****Database Commands*****
"""


@dbsetup.cli.command("seed")
def seed():
    from data.seed import Seed

    Seed().data()


@dbsetup.cli.command("minimal_seed")
def minimal_seed():
    from data.seed import Seed

    Seed().minimal_data()


@dbsetup.cli.command("create")
def create():
    """Creates database tables"""
    db.create_all()


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
    from data.seed import Seed

    if click.confirm("Are you sure you want to lose all your data"):
        db.drop_all()
        db.create_all()
        Seed().data()


if __name__ == "__main__":
    import sys

    print(
        "'pipenv run python manage.py {}' ".format(sys.argv[1])
        + "has been deprecated\n"
        + "please use 'pipenv run flask db {}'".format(sys.argv[1])
    )
