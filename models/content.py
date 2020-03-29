from os import path

from models.note import NoteId


class Content:

    @staticmethod
    def _file(nid: NoteId):
        return path.join(*['./data', nid.project, 'content', f'{nid.id}.json'])

    @staticmethod
    def save(nid: NoteId, body: str):
        open(Content._file(nid), 'w').write(body) \


    @staticmethod
    def load(nid: NoteId):
        return open(Content._file(nid))
