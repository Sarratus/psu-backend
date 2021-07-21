import click

from flask import g, Blueprint

from .model import db


db_session = db.session
db_actions = Blueprint('db_actions', __name__)


def init_db():
    from . import model
    db.create_all()


def get_db():
    return db_session


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


@db_actions.cli.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    db.drop_all()
    init_db()
    click.echo('Initialized the database.')


@db_actions.cli.command('fill-db')
def fill_db_command():
    """Наполняет таблицы данными из data.txt (каталог: db_filler)"""

    import sys
    sys.path.append('..')
    from .db_filler.main import fill_out_db
    fill_out_db(db_session)
    click.echo('DB was successfully filled.')


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
