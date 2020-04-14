# Tests for default JsonStore class
import os
import shutil

from dachar.utils.json_store import _BaseJsonStore


# Create a new dummy store to run tests on
class _TestStore(_BaseJsonStore):

    store_name = 'TestStore'
    config = {'store_type': 'local',
              'local.base_dir': '/tmp/test-store',
              'local.dir_grouping_level': 4}
    mappers = {'*': '__all__'}
    required_fields = ['data']
    search_defaults = ['id', 'data']


recs = [
    ('1.2.3.4.5.6.b', {'data': 'great match'}),
    ('1.2.3.4.5.6.a', {'x': 'does not save'}),
    ('2.2.2.2.2.2.c', {'data': {'d2': {'test': 123, 'test2': 'hi'}}})
]

store = None

def _get_store():
    return _TestStore()

def setup_module():
    global store
    store = _TestStore()

def test_verify_store():
    # Tests that the store gets created - via setup_module()
    pass

def test_put():
    store.put(*recs[0])

def test_get():
    rec = store.get(recs[0][0])
    assert(rec == recs[0][1])

def test_delete():
    _id = recs[0][0]
    store.delete(_id)
    assert(store.get(_id) is None)

def test_validate_non_json():
    try:
        store._validate('rubbish')
    except Exception as exc:
        assert(str(exc) == 'Cannot serialise content to valid JSON.')

def test_put_fail_validate():
    try:
        store.put(*recs[1])
    except ValueError as exc:
        assert(str(exc).find('Required content "data" not found.') > -1)

def test_get_all_ids():
    store.put(*recs[0])
    store.put(*recs[2])
    all_ids = [_ for _ in store._get_all_ids()]
    assert(all_ids == [recs[0][0], recs[2][0]])

def test_search():
    # Search with default fields + exact match
    resp = store.search('great match', exact=True, fields=None, ignore_defaults=False)
    assert(resp == [recs[0][1]])

    # Search with custom fields + exact match
    resp = store.search('great match', exact=True, fields=['data'], ignore_defaults=True)
    assert(resp == [recs[0][1]])

    # Search with default fields + partial match
    resp = store.search('at MAT', exact=False, fields=None, ignore_defaults=False)
    assert(resp == [recs[0][1]])

    # Search with custom nested fields + exact match
    resp = store.search('123', exact=True, fields=['data.d2.test'], ignore_defaults=True)
    assert(resp == [recs[2][1]])

    # Search with default fields + partial match
    resp = store.search('123', exact=False, fields=None, ignore_defaults=False)
    assert(resp == [recs[2][1]])

    # Search with custom nested fields + exact match as integer
    resp = store.search(123, exact=True, fields=['data.d2.test'], ignore_defaults=True)
    assert(resp == [recs[2][1]])

    # Search with custom multiple fields and partial match
    resp = store.search('e', exact=False, fields=['data', 'data.d2.test'], ignore_defaults=True)
    assert(resp == [recs[0][1], recs[2][1]])

    # Search wih failed match
    resp = store.search('zzz', exact=False, fields=None, ignore_defaults=False)
    assert(resp == [])

def teardown_module():
    dr = _TestStore.config['local.base_dir']
    if os.path.isdir(dr):
        shutil.rmtree(dr)
