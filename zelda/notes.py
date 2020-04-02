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


@bp.route('/import', methods=('GET', 'POST'))
@login_required
def create():
    """
    Either the form is displayed,
    or the posted data is validated and the post is added to the database
    or an error is shown.
    See https://flask.palletsprojects.com/en/1.1.x/tutorial/blog/
    """
    if request.method == 'POST':
        title = request.form['folder']
        error = None

        if not folder:
            error = 'Folder is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO post (title, body, author_id)'
                ' VALUES (?, ?, ?)',
                (title, body, g.user['id'])
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('notes/import.html')