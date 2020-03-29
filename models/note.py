from datetime import datetime
from dataclasses import dataclass

from models.content import Contents
from models.project import Project


@dataclass
class Markup:
    raw: str

    def snippet(self, chars=20):
        return self.raw[100:(100+chars)]


@dataclass
class Timestamp:
    # For example, 5:42:09 PM GMT on January 20th, 2007 would be encoded as: 20070120T174209Z
    # “Z”: stands for Zero timezone (UTC+0) (see RFC 3339)
    # https://stackoverflow.com/questions/10286204/the-right-json-date-format
    #return datetime(int(t[0:4]), int(t[4:6]), int(t[6:8]), int(t[9:11]),
    #                int(t[11:13]), int(t[13:15]), 0, timezone.utc)
    # https://www.w3.org/TR/NOTE-datetime

    as_datetime: datetime

    json_date_format = '%Y%m%dT%H%M%SZ'

    @staticmethod
    def read(in_json_date_format):
        return Timestamp(datetime.strptime(in_json_date_format))

    def write(self):
        return self.as_datetime.strftime(Timestamp.json_date_format)

@dataclass
class NoteId:
    id: int
    project: str


@dataclass
class Note:
    id: NoteId  # local id assigned at import; unique across projects
    title: str = None
    created: Timestamp = None
    updated: Timestamp = None

    def content(self):
        Contents.load(self.id)

    def to_dict(self, content=False):

        assert not content

        return {
            'id': self.id,
            'title': self.title,
            'updated': self.updated.write()
        }


    # @staticmethod
    # def from_dict(d):
    #    return Note(*d)




