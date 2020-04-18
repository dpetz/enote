from os import getcwd
from os.path import join, exists
from app import models
from flask import Blueprint, flash, redirect, render_template, request, url_for, abort
from app.util import ImportNotesDB
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
def import_notes():
    """
    If GET, form page is rendered.
    If POST, form data is validated and the post is added to the database
    Flashes message if data is invalid.
    """
    if request.method == 'POST':
        file = request.form['file']

        if file:
            file = join(getcwd(), file)
            if exists(file):
                ImportNotesDB().import_from_path(file)
                return redirect(url_for('web.index'))

        flash(f'Not a file or path: {file}')

    return render_template('note/import.html')



