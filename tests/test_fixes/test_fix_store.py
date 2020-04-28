import os
import shutil

# Create a new dummy store to run tests on
from tests._stores_for_tests import _TestFixStore

recs = [
    {'fix_id': 'Fix1', 'operands': {'arg1': '1'}, 'ncml': '<NcML1>'},
    {'fix_id': 'Fix2', 'operands': {'arg2': '2'}, 'ncml': '<NcML2>'}
]


store = None


def _clear_store():
    dr = _TestFixStore.config['local.base_dir']
    if os.path.isdir(dr):
        shutil.rmtree(dr)


def setup_module():
    _clear_store()
    global store
    store = _TestFixStore()


def test_publish_fix_1():
    _id = 'ds.1.1.1.1.1.1'
    store.publish_fix(_id, recs[0])

    assert(store.get(_id)['fixes'] == [recs[0]])


def test_publish_fix_2():
    _id = 'ds.1.1.1.1.1.2'
    store.publish_fix(_id, recs[1])
    assert(store.get(_id)['fixes'] == [recs[1]])

    _id = 'ds.1.1.1.1.1.1'
    store.publish_fix(_id, recs[1])
    assert(store.get(_id)['fixes'] == [recs[0], recs[1]])


def test_withdraw_fix_1():
    _id = 'ds.1.1.1.1.1.1'
    store.withdraw_fix(_id, 'Fix1')
    assert(store.get(_id)['fixes'] == [recs[1]])

    store.withdraw_fix(_id, 'Fix2')
    assert(store.exists(_id) is False)


def teardown_module():
    _clear_store()
