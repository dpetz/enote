import json
from dataclasses import dataclass
from shutil import rmtree
from xml.etree import ElementTree
from os.path import join, isfile, exists
from os import listdir, makedirs, getcwd
from datetime import datetime
from app.db import get_db
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


def import_notes_to_handler(path, handler):
    """ Import notes from XML file generated via export from Evernote client
    :param path: file (absolute or relative to project folder) or folder (to import all files recursively)
    :param handler: function to be called for each notes. Must have named argument for each note element
    :return: number of imported notes
    """

    path = join(getcwd(), path)
    counter = 0

    # If path is folder recurse
    if not isfile(path):
        for f in listdir(path):
            counter += import_notes(path.join(path, f))
        return counter

    # Otherwise parses XML by calling handler for every note element encountered.

    # see https://docs.python.org/3/library/xml.etree.elementtree.html
    elements = ElementTree.parse(path).iter()

    # from DTD: (title, content, created?, updated?, tag*, note-attributes?, resource*)
    note_child_tags = ['title', 'content', 'created', 'updated', 'note-attributes', 'resource']

    while True:
        try:
            e = next(elements)
            if e.tag == 'note':
                title, created, updated, content = None, None, None, None
                while True:
                    e = next(elements)
                    if e.tag in note_child_tags:
                        if e.tag == 'title':
                            title = e.text
                        elif e.tag == 'created':
                            created = from_iso_8601(e.text)
                        elif e.tag == 'updated':
                            updated = from_iso_8601(e.text)
                        elif e.tag == 'content':
                            content = e.text
                    else:
                        handler(title, created, updated, content)
                        break
                counter += 1
        except StopIteration:
            break

    return counter


def import_toc(file='import/toc.enex'):
    """ Reads a file containing an exported table of content note.
          Based on it creates/updates a mapping from note titles to note URIs
          which can be used resolve links between notes.
          Assumes table contains all notes added in application and titles did not change.
          For Evernote's link types see https://dev.evernote.com/doc/articles/note_links.php

    :param file: File to import from. Defaults to '[PROJECT_FOLDER]/import/toc.enex'
    :return: Dictionary of GUIDs to titles
    """

    toc_content = None

    def handler(title, created, updated, content):
        nonlocal toc_content
        assert not toc_content, "File contains more than one note"
        toc_content = content

    import_notes_to_handler(file, handler)

    html = BeautifulSoup(toc_content, 'html.parser')

    tags = html.find_all('a', {'href': re.compile('^evernote')})

    return dict((extract_guid(tag.get('href')), tag.text) for tag in tags)


def extract_guid(link):
    """ Works for note links like
        evernote:///view/[userId]/[shardId]/[noteGuid]/[noteGuid]/
        and for in app links like
        https://[service]/shard/[shardId]/nl/[userId]/[noteGuid]/
        Assumes GUIDs have format https://de.wikipedia.org/wiki/Globally_Unique_Identifier
        """
    return re.compile(r'[a-f\d-]+/?$').search(link).group(0).replace('/', '')


# print(len(GuidIndex().titles_by_guid))
