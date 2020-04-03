from os import listdir, makedirs, getcwd
from os.path import join, isfile, exists
from shutil import rmtree
from datetime import datetime
from xml.etree import ElementTree
from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify, abort
from zelda.db import get_db
import json

bp = Blueprint('note', __name__, url_prefix='/note')


@bp.route('/')
def index():
    return redirect(url_for('note.list_html'))


@bp.route('/api/list')
def list_json():
    """ Json list all notes as dictionaries """

    return fetchall_into_json_response(get_db().execute(
        'SELECT id, title, created, updated'
        ' FROM note ORDER BY updated DESC'
    ))


def fetchall_into_json_response(cursor):
    return jsonify([dict(zip([column[0] for column in cursor.description], row))
                for row in cursor.fetchall()])


def fetchone_into_json_response(cursor):
    return jsonify(dict(zip([column[0] for column in cursor.description], cursor.fetchone())))


def get_note(id):
    note = fetchone_into_json_response(get_db().execute(
        'SELECT id, title, created, updated, content'
        ' FROM note WHERE id = ?',
        (id,)
    ))

    if note.data is None:
        abort(404, f"Note id {id} doesn't exist.")

    return note.get_json()


@bp.route('/web/list')
def list_html():
    """ List all notes"""
    return render_template('note/list.html', notes=list_json().get_json())


@bp.route('/web/<int:id>/view')
def view(id):
    return render_template('note/view.html', note=get_note(id))


@bp.route('/<int:id>/links')
def links(id):
    """"""
    pass


@bp.route('/add', methods=('GET', 'POST'))
def add():
    """
    Either the form is displayed,
    or the posted data is validated and the post is added to the database
    or an error is shown.
    See https://flask.palletsprojects.com/en/1.1.x/tutorial/blog/
    """
    if request.method == 'POST':
        file = request.form['file']

        if file:
            file = join(getcwd(), file)
            if exists(file):
                import_from_path(file)
                return redirect(url_for('note.index'))

        flash(f'Not a file or path: {file}')

    return render_template('note/add.html')


def import_from_path(path):
    # import each file in import folder

    if not isfile(path):
        for f in listdir(path):
            import_from_path(path.join(path, f))
    else:
        # https://docs.python.org/3/library/xml.etree.elementtree.html
        elements = ElementTree.parse(path).iter()
        e = next(elements)

        while True:
            try:
                if e.tag == 'note':
                    e = _import_note(elements)
                else:
                    e = next(elements)
            except StopIteration:
                break


@bp.route('/web/<int:id>/delete', methods=('POST',))
def delete_html(id):
    delete_json(id)
    return redirect(url_for('note.list_html'))

@bp.route('/api/<int:id>/delete', methods=('POST',))
def delete_json(id):
    get_note(id)
    db = get_db()
    db.execute('DELETE FROM note WHERE id = ?', (id,))
    db.commit()
    return jsonify(success=True)

# https://stackoverflow.com/questions/10286204/the-right-json-date-format
def from_iso_8601(json_date):
    return datetime.strptime(json_date, '%Y%m%dT%H%M%SZ')


def to_iso_8601(date_time):
    return date_time.strftime('%Y%m%dT%H%M%SZ')


def _import_note_attributes():
    # <!ELEMENT note-attributes
    # (subject-date?, latitude?, longitude?, altitude?, author?, source?,
    # source-url?, source-application?, reminder-order?, reminder-time?,
    # reminder-done-time?, place-name?, content-class?, application-data*)
    pass

def _import_resource():
    # <!ELEMENT resource
    # (data, mime, width?, height?, duration?, recognition?, resource-attributes?,
    # alternate-data?)
    pass


def _import_note(note_child_elements):

    # from DTD: (title, content, created?, updated?, tag*, note-attributes?, resource*)
    note_child_tags = ['title', 'content', 'created', 'updated', 'note-attributes', 'resource']

    while True:

        ne = next(note_child_elements)  # not element
        if ne.tag in note_child_tags:
            if ne.tag == 'title':
                title = ne.text
            elif ne.tag == 'created':
                created = from_iso_8601(ne.text)
            elif ne.tag == 'updated':
                updated = from_iso_8601(ne.text)
            elif ne.tag == 'content':
                content = ne.text

        else:
            db = get_db()
            db.execute(
                'INSERT INTO note (title, created, updated, content)'
                ' VALUES (?, ?, ?, ?)',
                (title, created, updated, content)
            )
            db.commit()
            return ne
