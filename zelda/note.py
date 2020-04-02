from os import listdir, makedirs, getcwd
from os.path import join, isfile, exists
from shutil import rmtree
from datetime import datetime


import xml.etree.ElementTree as ET

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from zelda.db import get_db

bp = Blueprint('note', __name__, url_prefix='/note')

folders = dict( (f, join('./data', f)) for f in ['resources'])


@bp.route('/')
def index():
    db = get_db()
    all_notes = db.execute(
        'SELECT id, title, updated'
        ' FROM note ORDER BY updated DESC'
    ).fetchall()
    return render_template('note/index.html', notes=all_notes)


@bp.route('/<int:id>/links')
def links(id):
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
        elements = ET.parse(path).iter()
        e = next(elements)

        while True:
            try:
                if e.tag == 'note':
                    e = _import_note(elements)
                else:
                    e = next(elements)
            except StopIteration:
                break


# https://stackoverflow.com/questions/10286204/the-right-json-date-format
def from_iso_8601(json_date):
    return datetime.strptime(json_date, '%Y%m%dT%H%M%SZ')


def to_iso_8601(date_time):
    return date_time.strftime('%Y%m%dT%H%M%SZ')


def _import_note(note_child_elements):

    # from DTD: (title, content, created?, updated?, tag*, note-attributes?, resource*)
    note_child_tags = ['title', 'content', 'created', 'updated', 'note-attributes', 'resource']


    while True:

        ne = next(note_child_elements) # not element
        if ne.tag in note_child_tags:
            if ne.tag == 'title':
                title = ne.text
            elif ne.tag == 'updated':
                updated = from_iso_8601(ne.text)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO note (title, updated)'
                ' VALUES (?, ?)',
                (title, updated)
            )
            db.commit()
            return ne


def clear():
    """Delete all imported notes and related/derived resources"""

    # empty/create all project folders (except import folder)
    for d in folders.values():
            rmtree(d)
            makedirs(d)
