from flask import (
    Blueprint, flash, g,
    redirect, render_template,
    request, session, url_for,
)
from sqlalchemy import select, text
from flask.views import MethodView
from werkzeug.security import check_password_hash, generate_password_hash

from ..model import Client, Game, Review
from ..db import get_db, db_session


bp_games = Blueprint('games', __name__, url_prefix='/games')


class GameAPI(MethodView):
    def get(self, game_id):
        if game_id is None:
            games = Game.query.all()
            return render_template('games/games.html', games=games)
        else:
            game = Game.query.filter_by(id=game_id).first()
            client = g.client

            review = Review.query.filter_by(game=game, client=client).first()

            return render_template('games/game.html', game=game, review=review)

    def post(self, game_id):
        rating = int(request.form['rating'])
        review_text = request.form['review']

        client = g.client
        game = Game.query.filter_by(id=game_id).first()

        prev_review = Review.query.filter_by(game=game, client=client).first()
        review = Review(rating=rating, client=client, game=game, review_text=review_text)

        if prev_review:
            db_session.delete(prev_review)
            flash(u'Успешно обновлено')

        db_session.add(review)
        db_session.commit()
        return render_template('games/game.html', game=game, review=review)




    def delete(self, user_id):
        # delete a single user
        pass

    def put(self, user_id):
        # update a single user
        pass

game_view = GameAPI.as_view('game_api')

bp_games.add_url_rule('/', defaults={'game_id': None}, view_func=game_view, methods=['GET',])
bp_games.add_url_rule('/add', view_func=game_view, methods=['POST',])
bp_games.add_url_rule('/<int:game_id>', view_func=game_view, methods=['GET', 'POST',])
