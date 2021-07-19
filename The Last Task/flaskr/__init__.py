import os

from flask import Flask

from dotenv import load_dotenv
load_dotenv(dotenv_path='.env', override=True)


def create_app():
    """App-factory для удобства работы с config-файлами"""
    # init flask APP
    app = Flask(__name__, instance_relative_config=True)

    app.jinja_env.auto_reload = True
    app.config.from_mapping(
        SECRET_KEY='dev',
        SQLALCHEMY_DATABASE_URI=f'postgresql+psycopg2://'
                                f'{os.environ["DB_USER"]}:'
                                f'{os.environ["DB_PASSWORD"]}'
                                f'@localhost/db',
        TEMPLATES_AUTO_RELOAD=True,
    )

    # generate instance path
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # init DB
    from . import db
    db.init_app(app=app)

    # importing blueprints
    from . import auth
    app.register_blueprint(auth.bp_auth)

    return app
