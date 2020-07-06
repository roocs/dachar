# Tests for default JsonStore class
import os
import shutil

import pytest

from dachar.utils.json_store import _LocalBaseJsonStore


# Create a new dummy store to run tests on
class _TestStore(_LocalBaseJsonStore):

    store_name = 'TestStore'
    config = {'store_type': 'local',
              'local.base_dir': '/tmp/test-store',
              'local.dir_grouping_level': 4}
    required_fields = ['data']


recs = [
    ("1.2.3.4.5.6.b", {"data": "great match"}),
    ("1.2.3.4.5.6.a", {"x": "does not save"}),
    ("2.2.2.2.2.2.c", {"data": {"d2": {"test": 123, "test2": "hi"}}}),
]

store = None


def _clear_store():
    dr = _TestStore.config['local.base_dir']
    if os.path.isdir(dr):
        shutil.rmtree(dr)


def setup_module():
    _clear_store()
    global store
    store = _TestStore()


def test_verify_store():
    # Tests that the store gets created - via setup_module()
    pass


def test_put_fails_if_id_causes_unsafe_path():
    try:
        store.put('unsafe', recs[0][1])
    except KeyError as exc:
        assert(str(exc) == "'Identifier name cannot be safely translated to file path: unsafe'")


def test_put():
    _id, content = recs[0]
    store.put(_id, content)
    fpath = store._id_to_path(_id)
    os.path.isfile(fpath)


def test_put_force_parameter():
    _id, content = recs[0]
    if not store.exists(_id):
        store.put(_id, content)

    try:
        store.put(_id, content)
    except FileExistsError as exc:
        assert(str(exc) == f'Record already exists: {_id}. Use "force=True" to overwrite.')

    store.put(_id, content, force=True)


def test_put_maps_asterisk():
    _id = "1.1.*.1.*.*.1"
    store.put(_id, {"data": "test"})
    fpath = store._id_to_path(_id)

    bdir = store.config['local.base_dir']
    assert(fpath == os.path.join(bdir, '1/1/__ALL__/1.__ALL__.__ALL__.1.json'))
    assert(os.path.isfile(fpath))

    store.delete(_id)


def test_get():
    rec = store.get(recs[0][0])
    assert rec == recs[0][1]


def test_delete():
    _id = recs[0][0]
    store.delete(_id)
    assert store.get(_id) is None

    # Check that directories also get pruned
    dr = os.path.dirname(store._id_to_path(_id))
    while len(dr) > len(store.config["local.base_dir"]):
        assert not os.path.exists(dr)
        dr = os.path.dirname(dr)


def test_validate_non_json():
    try:
        store._validate("rubbish")
    except Exception as exc:
        assert str(exc) == "Cannot serialise content to valid JSON."


def test_put_fail_validate():
    try:
        store.put(*recs[1])
    except ValueError as exc:
        assert str(exc).find('Required content "data" not found.') > -1


# @pytest.mark.xfail(reason="tox test fails")
def test_get_all_ids():
    store.put(*recs[0])
    store.put(*recs[2])
    all_ids = [_ for _ in store.get_all_ids()]
    assert(all_ids == [recs[0][0], recs[2][0]])


# @pytest.mark.xfail(reason="tox test fails")
def test_search_by_term():
    # Search with custom fields + exact match
    resp = store.search("great match", exact=True, fields=["data"])
    assert resp == [recs[0][1]]

    # Search with partial match
    resp = store.search("at MAT", exact=False, fields=["data", "id"])
    assert resp == [recs[0][1]]

    # Search with custom nested fields + exact match
    resp = store.search("123", exact=True, fields=["data.d2.test"])
    assert resp == [recs[2][1]]

    # Search with partial match
    resp = store.search("123", exact=False, fields=["data", "id"])
    assert resp == [recs[2][1]]

    # Search with custom nested fields + exact match as integer
    resp = store.search(123, exact=True, fields=["data.d2.test"])
    assert resp == [recs[2][1]]

    # Search with custom multiple fields and partial match
    resp = store.search("e", exact=False, fields=["data", "data.d2.test"])
    assert resp == [recs[0][1], recs[2][1]]

    # Search everything if no fields
    resp = store.search('e', exact=False, fields=None)
    assert(resp == [recs[0][1], recs[2][1]])

    # Search wih failed match
    resp = store.search("zzz", exact=False, fields=None)
    assert resp == []


# @pytest.mark.xfail(reason="tox test fails")
def test_search_by_id():
    # Search for non-existent id
    resp = store.search("zzz", exact=False, match_ids=True)
    assert resp == []

    # Search by partial ID
    resp = store.search("5.6.b", exact=False, match_ids=True)
    assert resp == [recs[0][1]]

    # Search for exact ID
    resp = store.search(recs[0][0], exact=True, match_ids=True)
    assert resp == [recs[0][1]]


def teardown_module():
    _clear_store()
