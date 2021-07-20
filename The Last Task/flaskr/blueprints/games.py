from flask import (
    Blueprint, flash, g,
    redirect, render_template,
    request, session, url_for,
)
from sqlalchemy import select, text
from flask.views import MethodView
from werkzeug.security import check_password_hash, generate_password_hash

from ..model import Client, Game, Review, Developer, Publisher
from ..db import get_db, db_session
import datetime


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
        if request.form['submit'] == 'review':
            rating = int(request.form['rating'])
            review_text = request.form['review']

            client = g.client
            game = Game.query.filter_by(id=game_id).first()

            prev_review = Review.query.filter_by(game=game, client=client).first()

            if prev_review:
                Review.query.filter_by(game=game, client=client).update(dict(
                    date_of_review=datetime.datetime.now(),
                    rating=rating,
                    review_text=review_text
                ))
                flash(u'Успешно обновлено')
            else:
                review = Review(rating=rating, client=client, game=game, review_text=review_text)
                db_session.add(review)

            db_session.commit()
            review = Review(rating=rating, client=client, game=game, review_text=review_text)
            return render_template('games/game.html', game=game, review=review)

        if request.form['submit'] == 'delete':
            game = Game.query.filter_by(id=game_id).first()

            db_session.delete(game)
            db_session.commit()

            flash(u'Игра {} была удалена.'.format(game.title))

            return redirect(url_for('games.game_api', game_id=None))

    def delete(self, game_id):
        pass



game_view = GameAPI.as_view('game_api')

bp_games.add_url_rule('/', defaults={'game_id': None}, view_func=game_view, methods=['GET',])
bp_games.add_url_rule('/<int:game_id>', view_func=game_view, methods=['GET', 'POST',])


@bp_games.route('/add', methods=('GET', 'POST'))
def add_game():
    if request.method == 'POST':
        title = request.form['title']
        release_date = request.form['release_date']
        developer = request.form['developer']
        publisher = request.form['publisher']

        game = Game(
            title=title,
            release_date=release_date,
            developer=Developer.get_or_create(name=developer, session=db_session),
            publisher=Publisher.get_or_create(name=publisher, session=db_session),
        )

        db_session.add(game)
        db_session.commit()

        flash(u'Game {} has been added.'.format(title))

        return redirect(url_for('games.game_api', game_id=None))
    else:
        return render_template('games/add_form.html')
