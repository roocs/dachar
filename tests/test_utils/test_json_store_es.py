# Tests for default JsonStore class
import os
import shutil
import pytest

from dachar.utils.json_store import _BaseJsonStore


# Create a new dummy store to run tests on
class _TestStore(_BaseJsonStore):

    store_name = 'TestElasticsearchStore'
    config = {'store_type': 'elasticsearch',
              'local.base_dir': '/tmp/test-store',
              'local.dir_grouping_level': 4,
              'index': 'char-store-test'}
    id_mappers = {'*': '__ALL__'}
    required_fields = ['d']
    search_defaults = ['id', 'data']


store = None

recs = [
    ('1.2.3.4.5.6.b', {'d': 'great match'}),
    ('1.2.3.4.5.6.a', {'x': 'does not save'}),
    ('1.2.3.4.5.6.c', {'d': 'cool'})
]


def clear_store():
    for id in recs[0][0], recs[1][0], recs[2][0]:
        try:
            store.delete(id)
        except Exception:
            pass


def setup_module():
    # check elasticsearch connection - if fails - fail all tests
    global store
    store = _TestStore()
    clear_store()


def test_verify_store():
    # Tests that the store gets created - via setup_module()
    pass


def test_get():
    rec = store.get('cmip5.output1.INM.inmcm4.historical.mon.atmos.Amon.r1i1p1.latest.tas.json')
    assert rec['variable']['var_id'] == 'tas'


def test_put():
    _id, content = recs[0]
    store.put(_id, content)
    assert store.exists(_id)


def test_put_force_parameter():
    _id, content = recs[0]
    if not store.exists(_id):
        store.put(_id, content)

    with pytest.raises(FileExistsError) as exc:
        store.put(_id, content)
        assert str(exc.value) == f'Record already exists: {_id}. Use "force=True" to overwrite.'

    store.put(_id, content, force=True)


# def test_put_maps_asterisk():
#     _id = '1.1.*.1.*.*.1'
#     store.put(_id, {'data': 'test'})
#     fpath = store._id_to_path(_id)
#
#     bdir = store.config['local.base_dir']
#     assert(fpath == os.path.join(bdir, '1/1/__ALL__/1.__ALL__.__ALL__.1.json'))
#     assert(os.path.isfile(fpath))
#     store.delete(_id)


def test_delete():
    _id, content = recs[2]
    store.put(_id, content)
    assert store.exists(_id)

    store.delete(_id)
    assert store.get(_id) is None


def test_validate_non_json():
    with pytest.raises(Exception) as exc:
        store._validate('rubbish')
        assert str(exc.value) == 'Cannot serialise content to valid JSON.'


def test_put_fail_validate():
    with pytest.raises(ValueError) as exc:
        store.put(*recs[1])
        assert(str(exc.value).find('Required content "d" not found.') > -1)


def test_get_all_ids():
    store.put(*recs[0])
    store.put(*recs[2])
    all = store.get_all()
    print(all)


def teardown_module():
    clear_store()
