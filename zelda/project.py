
import xml.etree.ElementTree as ET
import json
from os import path, listdir, makedirs
from shutil import rmtree

from zelda.note import Note, Timestamp, NoteId


class Project:

    def __init__(self, project):
        """Init project by name by loading data from sub-folder in data of same name"""

        self.project = project
        self.folders = dict( (f, path.join('./data', *[project, f]))
                             for f in ['import', 'contents', 'notes'])

        notes_file = path.join(self.folders['notes'], 'all,json')

        if path.exists(notes_file):
            self.notes = [Note(json.load(notes_file).update('project', project))]

        else:  # import project

            import_folder = self.folders['import']

            # empty/create all project folders (except import folder)
            for d in self.folders.values():
                if d != import_folder:
                    rmtree(d)
                    makedirs(d)

            # import each file in import folder
            self.notes = []
            for f in listdir(import_folder):
                file = path.join(import_folder, f)
                assert path.isfile(file), f"Not a file: {file}"
                self._import_file(file, self.notes, self)

            open(notes_file, 'w').write(json.dumps([n.to_dict() for n in self.notes], indent=4))

    def __iter__(self):
        return self.notes.__iter__()

    @staticmethod
    def _import_file(file, notes, project):

        # from DTD: (title, content, created?, updated?, tag*, note-attributes?, resource*)
        note_child_tags = ['title', 'content', 'created', 'updated', 'note-attributes', 'resource']

        def _import_note(note_child_elements):

            n = Note(NoteId(len(notes+1), project))

            while True:
                ne = next(note_child_elements)
                if ne.tag in note_child_tags:
                    if ne.tag == 'title':
                        n.title = ne.text
                    elif ne.tag == 'created':
                        n.created = Timestamp.read(ne.text)
                    elif ne.tag == 'updated':
                        n.updated = Timestamp.read(ne.text)
                    elif ne.tag == 'content':
                        Contents.save(n, ne.text)
                else:
                    notes.append(n)
                    return ne

        # https://docs.python.org/3/library/xml.etree.elementtree.html
        elements = ET.parse(file).iter()
        e = next(elements)

        while True:
            try:
                if e.tag == 'note':
                    e = _import_note(elements)
                else:
                    e = next(elements)

            except StopIteration:

                break


for note in Project('test1'):
    print(note.to_dict())
