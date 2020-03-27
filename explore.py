
import datetime
import xml.etree.ElementTree as ET
from dataclasses import dataclass


root = tree.


@dataclass
class Note:

    title: str
    created: datetime


class Pointer:
    """Wraps iterator. self.current resp. self.next point to current resp. next element """

    def __init__(self, iter):
        self.iter = iter
        self.current = next(iter)
        self.next = next(iter)


    def step(self):
        tmp = self.current
        self.current = self.next
        try:
            self.next = next(self.iter)
        except StopIteration:
            self.next = None
        return tmp



def import_enex(file='./data/Samples_3.enex'):

    # https://docs.python.org/3/library/xml.etree.elementtree.html
    pointer = Pointer(ET.parse(file).iter())
    notes = []

    while pointer.current:
        if pointer.current.tag == 'note':
                notes.append(import_note(pointer))

def import_note(current_element, element_iterator):

        assert pointer.current.tag == 'note'

        while pointer.next & pointer.next.

        e = next(element_iterator_inside_note)

        note = Note()

        if e.get('title'):
            note.title = e.text

        # note_elem.utcfromtimestamp(elem.get('created').text)



        yield Note(
            note_elem.get('title').text,

        )


for note in import_notes_from_xml(root.iter()):
    print(note)



def count_lines(file='./data/Samples_3.enex'):
    line_chars = []

    for line in open(file):
        line_chars.append(len(line))

    print(f'{len(line_chars)} lines: {line_chars[:100]}')

