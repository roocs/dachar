import os
import shutil

from tests._stores_for_tests import _TestFixProposalStore
from dachar.fixes import process_fixes
from dachar.utils.common import now_string

from unittest.mock import Mock

ds_ids = ['ds.1.1.1.1.1.1',
          'ds.2.1.1.1.1.1',
          'ds.3.1.1.1.1.1']

fixes = [
    {'fix_id': 'Fix1',
     'title': 'Apply Fix 1',
     'description': 'Applies fix 1',
     'category': 'test_fixes',
     'reference_implementation': 'daops.test.test_fix1',
     'operands': {'arg1': '1'}},
    {'fix_id': 'Fix2',
     'title': 'Apply Fix 2',
     'description': 'Applies fix 2',
     'category': 'test_fixes',
     'reference_implementation': 'daops.test.test_fix2',
     'operands': {'arg2': '2'}},
]

prop_store = None


def clear_stores():
    fp_dr = _TestFixProposalStore.config['local.base_dir']
    if os.path.isdir(fp_dr):
        shutil.rmtree(fp_dr)


def setup_module():
    clear_stores()
    global prop_store
    prop_store = _TestFixProposalStore()


def generate_fix_proposal(id, fix):
    prop_store.propose(id, fix)


def generate_published_fix(id, fix):
    prop_store.publish(id, fix)


# tests 2 proposed fixes returned
def test_get_2_proposed_fixes():
    generate_fix_proposal('ds.1.1.1.1.1.1', fixes[0])
    generate_fix_proposal('ds.2.1.1.1.1.1', fixes[1])

    process_fixes.get_fix_prop_store = Mock(return_value=prop_store)

    proposed_fixes = process_fixes.get_proposed_fixes()

    assert len(proposed_fixes) == 2

    assert (proposed_fixes[0]) == {'dataset_id': 'ds.1.1.1.1.1.1',
                                   'fixes':
                                       [{'fix':
                                             {'category': 'test_fixes',
                                              'description': 'Applies fix 1',
                                              'fix_id': 'Fix1', 'operands': {'arg1': '1'},
                                              'reference_implementation': 'daops.test.test_fix1',
                                              'title': 'Apply Fix 1'},
                                         'history': [],
                                         'reason': '',
                                         'status': 'proposed',
                                         'timestamp': now_string()}]}

    assert proposed_fixes[1] == {'dataset_id': 'ds.2.1.1.1.1.1',
                                 'fixes':
                                     [{'fix':
                                           {'category': 'test_fixes',
                                            'description': 'Applies fix 2',
                                            'fix_id': 'Fix2',
                                            'operands': {'arg2': '2'},
                                            'reference_implementation': 'daops.test.test_fix2',
                                            'title': 'Apply Fix 2'},
                                       'history': [],
                                       'reason': '',
                                       'status': 'proposed',
                                       'timestamp': now_string()}]}


# tests only one proposed fix returned as other fix is now published
def test_get_1_proposed_fixes():

    generate_published_fix('ds.2.1.1.1.1.1', fixes[1])

    process_fixes.get_fix_prop_store = Mock(return_value=prop_store)

    proposed_fixes = process_fixes.get_proposed_fixes()

    assert prop_store.exists(ds_ids[0])
    assert prop_store.exists(ds_ids[1])
    assert len(proposed_fixes) == 1
    assert proposed_fixes[0] == {'dataset_id': 'ds.1.1.1.1.1.1',
                                 'fixes':
                                     [{'fix':
                                           {'category': 'test_fixes',
                                            'description': 'Applies fix 1',
                                            'fix_id': 'Fix1',
                                            'operands': {'arg1': '1'},
                                            'reference_implementation': 'daops.test.test_fix1',
                                            'title': 'Apply Fix 1'},
                                       'history': [],
                                       'reason': '',
                                       'status': 'proposed',
                                       'timestamp': now_string()}]}


def teardown_module():
    pass
    # clear_stores()
