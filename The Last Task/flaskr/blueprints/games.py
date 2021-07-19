from flask import (
    Blueprint, flash, g,
    redirect, render_template,
    request, session, url_for,
)
from sqlalchemy import select, text
from flask.views import MethodView
from werkzeug.security import check_password_hash, generate_password_hash

from ..model import Client, Game
from ..db import get_db, db_session


bp_games = Blueprint('game', __name__, url_prefix='/game')


@bp_games.route('/register', methods=('GET', 'POST'))
def get_game():
    pass


class GameAPI(MethodView):
    def get(self, game_id):
        if game_id is None:
            games = Game.query.all()
        else:
            game = Game.query.filter_by(id=game_id)

    def post(self):
        # create a new user
        pass

    def delete(self, user_id):
        # delete a single user
        pass

    def put(self, user_id):
        # update a single user
        pass

game_view = GameAPI.as_view('game_api')

bp_games.add_url_rule('/', defaults={'game_id': None}, view_func=game_view, methods=['GET',])
bp_games.add_url_rule('/', view_func=game_view, methods=['POST',])
bp_games.add_url_rule('/<int:game_id>', view_func=game_view, methods=['GET', 'PUT', 'DELETE'])
