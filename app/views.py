from app import models
from flask import Blueprint, flash, redirect, render_template, request, url_for, abort
import requests
bp = Blueprint('web', __name__, url_prefix='/')


@bp.route('/')
def index():
    """ Page with a list of all notes. """
    return render_template('note/index.html', notes=models.notes().get_json())


@bp.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    requests.delete( url_for('v1.note', id=id, _external=True))
    return redirect(url_for('web.index'))


@bp.route('/<int:id>')
def note(id):

    response = models.note(id)

    if response.data is None:
        abort(404, f"Note id {id} does not exist.")

    return render_template('note/note.html', note=response.get_json())


@bp.route('/import', methods=('GET', 'POST'))
def import_():
    """
    If GET, form page is rendered.
    If POST, form data is validated and the post is added to the database
    Flashes message if data is invalid.
    """
    if request.method == 'GET':
        return render_template('note/import.html')

    else:  # POST
        path = request.form['path']
        r = requests.post(url_for('v1.import_notes', path=path, _external=True))
        try:
            flash(r.get_json()['imported'] + " notes imported.")
        except AttributeError:
            flash(f"Error:{r.content}", 'error')
        return redirect(url_for('web.index'))




