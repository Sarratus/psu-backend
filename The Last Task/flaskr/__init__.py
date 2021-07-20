import os

from flask import Flask, render_template

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
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    # generate instance path
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # init DB
    from .model import db as database
    database.init_app(app=app)
    # init DB commands
    from .db import db_actions
    app.register_blueprint(db_actions)

    # importing blueprints
    from .blueprints import auth, actions, games
    app.register_blueprint(auth.bp_auth)
    app.register_blueprint(actions.bp_actions)
    app.register_blueprint(games.bp_games)

    @app.route('/')
    def origin():
        return render_template('base.html')

    return app
