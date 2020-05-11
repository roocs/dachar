from dachar.analyse.checks.coord_checks import *
import os
import shutil

from tests._stores_for_tests import _TestDatasetCharacterStore, \
    _TestFixProposalStore
from dachar.scan.scan import scan_dataset, get_dataset_paths
from dachar.utils import options

char_store = None
prop_store = None

options.project_base_dirs['cmip5'] = \
    'tests/mini-esgf-data/test_data/badc/cmip5/data'

ds_ids = ['cmip5.output1.INM.inmcm4.rcp45.mon.ocean.Omon.r1i1p1.latest.zostoga',
          'cmip5.output1.MPI-M.MPI-ESM-LR.rcp45.mon.ocean.Omon.r1i1p1.latest.zostoga',
          'cmip5.output1.BCC.bcc-csm1-1.rcp45.mon.ocean.Omon.r1i1p1.latest.zostoga']


def clear_stores():
    fp_dr = _TestFixProposalStore.config['local.base_dir']
    dc_dr = _TestDatasetCharacterStore.config['local.base_dir']
    for dr in [fp_dr, dc_dr]:
        if os.path.isdir(dr):
            shutil.rmtree(dr)


# populate test character store
def populate_dc_store():
    ds_paths = get_dataset_paths('cmip5', ds_ids=ds_ids, paths=options.project_base_dirs['cmip5'])
    for ds_id, ds_path in ds_paths.items():
        character, ds_id = scan_dataset('cmip5', ds_id, ds_path, 'full', 'ceda')
        char_store.put(ds_id, character, force=True)


def setup_module():
    clear_stores()
    global char_store
    global prop_store

    char_store = _TestDatasetCharacterStore()
    prop_store = _TestFixProposalStore()

    populate_dc_store()


def test_RankCheck():
    x = RankCheck(ds_ids)
    results, atypical_content, typical_content = x.run()
    assert atypical_content[0]['data.coord_names'] == ["lev", "time"]
    assert atypical_content[0]['data.shape'] == [1, 1140]
    assert typical_content['data.coord_names'] == ["time"]
    assert typical_content['data.shape'] == [3540]


def test_RankCheck_deduce_fix():
    x = RankCheck(ds_ids)
    results, atypical_content, typical_content = x.run()
    d = x.deduce_fix(results[atypical_content[0]], atypical_content[0], typical_content)
    assert (d['dataset_id']['ds_id'] ==
            ['cmip5.output1.INM.inmcm4.rcp45.mon.ocean.Omon.r1i1p1.latest.zostoga'])
    assert (d['fix']['fix_id']) == 'SqueezeDimensionsFix'
    assert (d['fix']['category']) == 'coord_fixes'
    assert (d['fix']['operands']) == {'dims': ['lev']}


def test_with_different_thresholds():
    """test with different results - want fix to be not be
    suitable and return none"""
    pass
