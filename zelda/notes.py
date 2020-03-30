import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from zelda.db import get_db

bp = Blueprint('notes', __name__, url_prefix='/notes')

@bp.route('/find', methods=('GET', 'POST'))
def find():
    if request.method == 'POST':
        title = request.form['Title']
        db = get_db()
        error = None

        note = db.execute(
            'SELECT id FROM user WHERE title = ?', (title,)
        ).fetchone()

        if not note:
            error = 'Note note found'

        if error is None:
            session.clear()
            session['note_id'] = note['id']
            return redirect(url_for('notes.view'))

            flash(error)

        return render_template('notes/find.html')

@bp.route('/view', methods=('GET', 'POST'))
def view():
    if request.method == 'POST':
        title = request.form['View Note']
        db = get_db()
        error = None

        (title, updated) = db.execute(
            'SELECT title, updated FROM user WHERE id = ?', (session['note_id'],)
        ).fetchone()


        return f'{title} was updated on {updated}'