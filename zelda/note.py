from os import listdir, makedirs, getcwd
from os.path import join, isfile, exists
from bs4 import BeautifulSoup
import re

from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify, abort
from zelda.db import get_db

from zelda.util import (
    fetchall_into_json_response,
    fetchone_into_json_response,
    ImportNotesDB,
    import_toc
)

bp = Blueprint('note', __name__, url_prefix='/note')


@bp.route('/')
def index():
    return redirect(url_for('note.list_html'))


@bp.route('/api/list')
def list_json():
    """ Json list all notes as dictionaries """
    cursor = get_db().execute(
        'SELECT id, title, created, updated'
        ' FROM note ORDER BY updated DESC'
    )
    return fetchall_into_json_response(cursor)


@bp.route('/api/<int:id>/view')
def view_api(id):
    cursor = get_db().execute(
        'SELECT id, title, created, updated, content'
        ' FROM note WHERE id = ?',
        (id,)
    )
    return fetchone_into_json_response(cursor)


@bp.route('/web/list')
def list_html():
    """ List all notes"""
    return render_template('note/list.html', notes=list_json().get_json())


@bp.route('/web/<int:id>/view')
def view_html(id):
    note = view_api(id)

    if note.data is None:
        abort(404, f"Note id {id} does not exist.")

    return render_template('note/view.html', note=note.get_json())


@bp.route('/api/<int:id>/links')
def links_json(id, content=None):
    """"""
    if not content:
        content = view_api(id).get_json()['content']

    soup = BeautifulSoup(content)

    links = {
        'external': [(link.get('href'), link.text) for link in
                     soup.findAll('a', attrs={'href': re.compile("^https?://")})],
        'internal': [(link.get('href'), link.text) for link in
                     soup.findAll('a', attrs={'href': re.compile("^evernote://")})],
    }

    return jsonify(links)


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
                ImportNotesDB().import_from_path(file)
                return redirect(url_for('note.index'))

        flash(f'Not a file or path: {file}')

    return render_template('note/add.html')


@bp.route('/web/<int:id>/delete', methods=('POST',))
def delete_html(id):
    delete_json(id)
    return redirect(url_for('note.list_html'))


@bp.route('/api/<int:id>/delete', methods=('POST',))
def delete_json(id):
    db = get_db()
    db.execute('DELETE FROM note WHERE id = ?', (id,))
    db.commit()
    return jsonify(success=True)


@bp.route('/api/toc', methods=('POST', 'GET', 'DELETE'))
def toc():
    """DELETE to wipe out the ToC.
       POST with file name adds the file to the ToC
       GET to return ToC entries """

    db = get_db()

    def size():
        return db.execute("SELECT COUNT(*) FROM toc").fetchone()[0]

    if request.method == 'GET':
        return fetchall_into_json_response(db.execute(
            'SELECT guid, title FROM toc'))

    elif request.method == 'DELETE':
        size = size()
        db.execute("DELETE FROM toc")
        db.commit()
        return {'deleted': size}

    else:  # POST

        file_param = request.form['file']
        # for GET this would be request.args instead
        # form.get('file') returns None while form['file'] will abort

        toc_file = join(getcwd(), file_param)
        if not isfile(toc_file):
            abort(404, f"File not found:{toc_file}")
        titles_by_guids = import_toc(toc_file)
        db.executemany("INSERT INTO toc (guid,title) VALUES (?, ?)", titles_by_guids.items())
        db.commit()
        return jsonify({
            'added': len(titles_by_guids),
            'source': toc_file,
            'total': size()
        })


@bp.route('/api/find')
def find():
    """Retrieves local id from DB. Raises KeyError otherwise."""

    guid = request.args.get('guid')
    title = request.args.get('title')
    content = request.args.get('content')

    if ((guid is not None) + (title is not None) + (content is not None)) != 1:
        abort(400, f"Need exactly one of following parameters: guid, title, content")

    if guid:
        title = get_db().execute(
            'SELECT title FROM toc WHERE guid=?', (guid,)
        ).fetchone()

        if not title:
            abort(404, f"Unknown GUID: {guid}")

        return fetchall_into_json_response(get_db().execute(
            "SELECT id, title, created, updated, imported, content"
            " FROM note WHERE title = ?",
            (title[0],)
        ))
    if title:
        return fetchall_into_json_response(get_db().execute(
            "SELECT id, title, created, updated, imported, content"
            " FROM note WHERE title LIKE ?",
            (title,)
        ))
    if content:
        return fetchall_into_json_response(get_db().execute(
            "SELECT id, title, created, updated, imported, content"
            " FROM note WHERE content LIKE ?",
            (content,)
        ))
