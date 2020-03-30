import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from zelda.db import get_db

bp = Blueprint('note', __name__, url_prefix='/note')


@bp.route('/')
def index():
    db = get_db()
    all_notes = db.execute(
        'SELECT id, title, updated'
        ' FROM note ORDER BY updated DESC'
    ).fetchall()
    return render_template('note/index.html', notes=all_notes)
