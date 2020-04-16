from zelda.util import extract_guid


def test_extract_guid():
    note_link = 'evernote:///view/536854/s1/73d53dcc-c4c3-40c6-aeff-55138da5ec26/73d53dcc-c4c3-40c6-aeff-55138da5ec26/'
    assert extract_guid(note_link) == '73d53dcc-c4c3-40c6-aeff-55138da5ec26'
    inapp_note_link = 'https://www.evernote.com/shard/s1//nl/536854/0c1ee56e-d792-4e01-9f71-9ecb13fdea30'
    assert extract_guid(inapp_note_link) == '0c1ee56e-d792-4e01-9f71-9ecb13fdea30'