import os
import shutil

from dachar.utils.common import now_string

# Create a new dummy store to run tests on
from tests._stores_for_tests import _TestFixProposalStore

fixes = [
    {'fix_id': 'Fix1', 'operands': {'arg1': '1'}, 'ncml': '<NcML1>'},
    {'fix_id': 'Fix2', 'operands': {'arg2': '2'}, 'ncml': '<NcML2>'},
    {'fix_id': 'Fix1', 'operands': {'DIFFERENT': 'CHANGED'}, 'ncml': '<NcMLDIFFERS>'}
]

store = None


def _clear_store():
    dr = _TestFixProposalStore.config['local.base_dir']
    if os.path.isdir(dr):
        shutil.rmtree(dr)


def setup_module():
    _clear_store()
    global store
    store = _TestFixProposalStore()


def test_propose():
    _id = 'ds.1.1.1.1.1.1'
    store.propose(_id, fixes[0])

    r = record = store.get(_id)
    found = r['fixes']
    assert(found[0]['status'] == 'proposed')
    assert(found[0]['fix'] == fixes[0])
    assert(found[0]['timestamp'].startswith(now_string()[:10]))
    assert(found[0]['history'] == [])
    assert(len(found) == 1)
    _clear_store()


def test_publish(do_clear=True):
    _id = 'ds.1.1.1.1.1.1'
    store.propose(_id, fixes[0])
    store.publish(_id, fixes[0])

    r = record = store.get(_id)
    found = r['fixes']
    assert(found[0]['status'] == 'published')
    assert(found[0]['fix'] == fixes[0])
    assert(found[0]['timestamp'].startswith(now_string()[:10]))

    history = found[0]['history']
    assert(len(history) == 1)
    assert(history[0]['status'] == 'proposed')
    assert(history[0]['reason'] == '')

    if do_clear:
        _clear_store()


def test_withdraw():
    test_publish(do_clear=False)

    _id = 'ds.1.1.1.1.1.1'
    store.withdraw(_id, fixes[0], reason='bad fix')

    r = record = store.get(_id)
    found = r['fixes']
    assert(found[0]['status'] == 'withdrawn')
    assert(found[0]['fix'] == fixes[0])
    assert(found[0]['timestamp'].startswith(now_string()[:10]))

    history = found[0]['history']
    assert(len(history) == 2)
    assert(history[0]['status'] == 'published')
    assert(history[0]['reason'] == '')

    _clear_store()


def test_publish_diff_operands():
    test_publish(do_clear=False)

    _id = 'ds.1.1.1.1.1.1'
    store.publish(_id, fixes[2])

    r = record = store.get(_id)
    found = r['fixes']
    assert(found[0]['status'] == 'published')
    assert(found[0]['fix'] == fixes[2])
    assert(found[0]['timestamp'].startswith(now_string()[:10]))

    history = found[0]['history']
    assert(len(history) == 2)
    assert(history[0]['status'] == 'published')
    assert(history[0]['reason'] == '')

    _clear_store()


def test_reject():
    _id = 'ds.1.1.1.1.1.1'
    store.propose(_id, fixes[0])
    store.reject(_id, fixes[0], reason='wrong')

    r = record = store.get(_id)
    found = r['fixes']
    assert(found[0]['status'] == 'rejected')
    assert(found[0]['reason'] == 'wrong')

    assert(found[0]['fix'] == fixes[0])
    assert(found[0]['timestamp'].startswith(now_string()[:10]))

    history = found[0]['history']
    assert(len(history) == 1)
    assert(history[0]['status'] == 'proposed')
    assert(history[0]['reason'] == '')

    _clear_store()


def test_publish_two_fixes():
    test_publish(do_clear=False)

    _id = 'ds.1.1.1.1.1.1'
    store.propose(_id, fixes[1])
    store.publish(_id, fixes[1])

    r = record = store.get(_id)
    found = r['fixes']

    assert(len(found) == 2)
    assert(found[1]['status'] == 'published')
    assert(found[1]['fix'] == fixes[1])
    assert(found[1]['timestamp'].startswith(now_string()[:10]))

    history = found[1]['history']
    assert(len(history) == 1)
    assert(history[0]['status'] == 'proposed')
    assert(history[0]['reason'] == '')

    _clear_store()


def teardown_module():
    _clear_store()
