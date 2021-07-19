from flask import (
    Blueprint, flash, g,
    redirect, render_template,
    request, session, url_for,
)
from sqlalchemy import select

from werkzeug.security import check_password_hash, generate_password_hash

from .model import Client
from .db import get_db, db_session

bp_auth = Blueprint('auth', __name__, url_prefix='/auth')


@bp_auth.before_app_request
def load_logged_in_user():
    client_id = session.get('client_id')

    if client_id is None:
        g.client = None
    else:
        g.client, = get_db().execute(
            select(Client).select_from(Client).filter_by(id=client_id)
        ).first()


@bp_auth.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        db = get_db()
        error = None

        if db.execute(
            select('*').select_from(Client).filter_by(username=username)
        ).fetchone() is not None:
            error = f"Client {username} is already registered."

        if error is None:
            new_client = Client(username, generate_password_hash(password))

            db_session.add(new_client)
            db_session.commit()

            return redirect(url_for('auth.login'))
        flash(error)

    return render_template('auth/register.html')


@bp_auth.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        if request.form['submit'] == 'login':
            username = request.form['username']
            password = request.form['password']

            db = get_db()
            error = None

            client, = db.execute(
                select(Client).select_from(Client).filter_by(username=username)
            ).first()

            if client is None:
                error = 'Incorrect username.'
            elif not check_password_hash(client.password, password):
                error = 'Incorrect password.'

            if error is None:
                session.clear()
                session['client_id'] = client.id
                return redirect(url_for('auth.login'))

            flash(error)

        if request.form['submit'] == 'logout':
            session.clear()
            return redirect(url_for('auth.login'))

    return render_template('auth/login.html')

@bp_auth.route('/action', methods=('GET', 'POST'))
def action():
    return render_template('action.html')
