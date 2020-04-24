import os
import shutil

from dachar.utils.common import now_string
from dachar.fixes.fix_proposal_store import FixProposalStore


# Create a new dummy store to run tests on
class _TestFixProposalStore(FixProposalStore):

    store_name = 'TestFixProposalStore'
    config = {'store_type': 'local',
              'local.base_dir': '/tmp/test-fix-proposal-store',
              'local.dir_grouping_level': 4}

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


def test_publish():
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
    assert(history[-1]['status'] == 'proposed')
    assert(history[-1]['reason'] == '')
    _clear_store()



def teardown_module():
    _clear_store()
