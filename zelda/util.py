import json
from shutil import rmtree
from xml.etree import ElementTree
from os.path import join, isfile, exists
from os import listdir, makedirs, getcwd
from datetime import datetime
from zelda.db import get_db
from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify, abort
from bs4 import BeautifulSoup
import re

def fetchall_into_json_response(cursor):
    return jsonify([dict(zip([column[0] for column in cursor.description], row))
                    for row in cursor.fetchall()])


def fetchone_into_json_response(cursor):
    return jsonify(dict(zip([column[0] for column in cursor.description], cursor.fetchone())))

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


def link_index():

    with open('/Users/dpetzoldt/git/home/zelda/zelda/data/import/index.enex', "r") as f:
        contents = f.read()
        soup = BeautifulSoup(contents, 'HTML')

        return dict((link.get('href'), link.text) for
                    link in soup.findAll('a', attrs={'href': re.compile("^evernote://")}))


print(link_index())