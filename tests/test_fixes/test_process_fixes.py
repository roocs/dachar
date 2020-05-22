import os
import shutil

from tests._stores_for_tests import _TestFixProposalStore, _TestFixStore
from dachar.fixes import process_fixes
from dachar.utils.common import now_string


from unittest.mock import Mock

ds_ids = ['ds.1.1.1.1.1.1',
          'ds.2.1.1.1.1.1',
          'ds.3.1.1.1.1.1',
          'ds.4.1.1.1.1.1']

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
    {'fix_id': 'Fix3',
     'title': 'Apply Fix 3',
     'description': 'Applies fix 3',
     'category': 'test_fixes',
     'reference_implementation': 'daops.test.test_fix3',
     'operands': {'arg3': '3'}},
    {'fix_id': 'Fix by id',
     'title': 'Apply Fix by id',
     'description': 'Applies fix ',
     'category': 'test_fixes',
     'reference_implementation': 'daops.test.test_fix_by_id',
     'operands': {'arg4': '4'}},
]

prop_store = None
f_store = None


def clear_stores():
    fp_dr = _TestFixProposalStore.config['local.base_dir']
    f_dr = _TestFixStore.config['local.base_dir']
    for dr in [fp_dr, f_dr]:
        if os.path.isdir(dr):
            shutil.rmtree(dr)


def setup_module():
    clear_stores()
    global prop_store
    global f_store
    prop_store = _TestFixProposalStore()
    f_store = _TestFixStore()


def generate_fix_proposal(id, fix):
    prop_store.propose(id, fix)


def generate_published_fix(id, fix):
    prop_store.publish(id, fix)


# tests 2 proposed fixes returned
def test_get_2_proposed_fixes():
    generate_fix_proposal(ds_ids[0], fixes[0])
    generate_fix_proposal(ds_ids[1], fixes[1])

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

    generate_published_fix(ds_ids[1], fixes[1])

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


def test_process_proposed_fixes():
    process_fixes.get_fix_prop_store = Mock(return_value=prop_store)
    process_fixes.get_fix_store = Mock(return_value=f_store)
    generate_fix_proposal(ds_ids[2], fixes[2])
    process_fixes.process_all_fixes()


def test_process_proposed_fixes_with_id():
    process_fixes.get_fix_prop_store = Mock(return_value=prop_store)
    process_fixes.get_fix_store = Mock(return_value=f_store)
    generate_fix_proposal(ds_ids[3], fixes[3])
    # process_fixes.process_all_fixes(ds_ids[2])
    process_fixes.process_all_fixes([ds_ids[3]])


def teardown_module():
    pass
    # clear_stores()
