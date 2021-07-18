from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

import os
import click

from flask import current_app, g
from flask.cli import with_appcontext


engine = create_engine(
    f"postgresql+psycopg2://"
    f"{os.environ['DB_USER']}:"
    f"{os.environ['DB_PASSWORD']}"
    f"@localhost/db",

    isolation_level="SERIALIZABLE",
)
db_session = scoped_session(sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine)
)
Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    from . import model
    Base.metadata.create_all(bind=engine)


def get_db():
    db_session = scoped_session(sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine)
    )

    return db_session


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
