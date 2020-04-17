from tests import client

def test_toc_empty(client):
    """Gets empty json """
    assert client.get('/v1/toc').get_json() == []


def test_toc_import(client):
    r = client.post('/v1/toc', data={'file': 'data/toc_100.enex'})
    assert int(r.get_json()['added']) == 100

    entry = client.get('/v1/toc').get_json()[1]
    assert entry['guid'] == '2df0f7b4-bec0-4005-a5ec-ebc3633ac303'
    assert entry['title'] == 'Kubernetes ConfigMaps and Secrets'


def test_toc_delete(client):
    test_toc_import(client)
    r = client.delete('/v1/toc')
    assert int(r.get_json()['deleted']) == 100
    test_toc_empty(client)
