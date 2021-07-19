from flask import (
    Blueprint, flash, g,
    redirect, render_template,
    request, session, url_for,
)
from sqlalchemy import select

from werkzeug.security import check_password_hash, generate_password_hash

from ..model import Client
from ..db import get_db, db_session


bp_actions = Blueprint('action', __name__, url_prefix='/action')
