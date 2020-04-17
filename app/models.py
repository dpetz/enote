from os import getcwd
from os.path import join, isfile, exists
from bs4 import BeautifulSoup
import re

from flask import Blueprint, flash, redirect, render_template, request, url_for, jsonify, abort
from app.db import get_db

from app.util import (
    fetchall_into_json_response,
    fetchone_into_json_response,
    ImportNotesDB,
    import_toc
)

bp = Blueprint('v1', __name__, url_prefix='/v1')


@bp.route('/notes')
def notes():
    """ Json response of list of all notes. """
    cursor = get_db().execute(
        'SELECT id, title, created, updated'
        ' FROM note ORDER BY updated DESC'
    )
    return fetchall_into_json_response(cursor)


@bp.route('/note/<int:id>', methods=('GET', 'DELETE'))
def note(id):

    if request.method == 'DELETE':
        db = get_db()
        db.execute('DELETE FROM note WHERE id = ?', (id,))
        db.commit()
        return jsonify(success=True)

    else:  # GET
        """Get note by ID as json response."""
        cursor = get_db().execute(
            'SELECT id, title, created, updated, content'
            ' FROM note WHERE id = ?',
            (id,)
        )
        return fetchone_into_json_response(cursor)


@bp.route('/toc', methods=('POST', 'GET', 'DELETE'))
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
            abort(404, f"Table of Contents file not found: {toc_file}")
        titles_by_guids = import_toc(toc_file)
        db.executemany("INSERT INTO toc (guid,title) VALUES (?, ?)", titles_by_guids.items())
        db.commit()
        return jsonify({
            'added': len(titles_by_guids),
            'source': toc_file,
            'total': size()
        })

@bp.route('/note/<int:id>/links')
def links(id, content=None):
    """"""
    if not content:
        content = note(id).get_json()['content']

    soup = BeautifulSoup(content)

    return jsonify({
        'external': [(link.note('href'), link.text) for link in
                     soup.findAll('a', attrs={'href': re.compile("^https?://")})],
        'internal': [(link.note('href'), link.text) for link in
                     soup.findAll('a', attrs={'href': re.compile("^evernote://")})],
    })


@bp.route('/find')
def find():
    """Get note by guid, title match, or content match.
       Exactly one of following parameters expected: guid, title, content."""

    guid = request.args.get('guid')
    title = request.args.get('title')
    content = request.args.get('content')

    if ((guid is not None) + (title is not None) + (content is not None)) != 1:
        abort(400, f"Exactly one of following parameters expected: guid, title, content")

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
