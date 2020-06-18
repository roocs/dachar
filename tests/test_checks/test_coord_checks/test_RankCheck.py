from dachar.analyse.checks.coord_checks import *
import os
import shutil

from tests._stores_for_tests import _TestDatasetCharacterStore, \
    _TestFixProposalStore
from dachar.scan.scan import scan_dataset, get_dataset_paths
from dachar.analyse.checks import _base_check
from dachar.utils import options
from unittest.mock import Mock
from dachar.scan import scan

char_store = None
prop_store = None

options.project_base_dirs['cmip5'] = \
    'tests/mini-esgf-data/test_data/badc/cmip5/data'

ds_ids = ['cmip5.output1.INM.inmcm4.rcp45.mon.ocean.Omon.r1i1p1.latest.zostoga',
          'cmip5.output1.MPI-M.MPI-ESM-LR.rcp45.mon.ocean.Omon.r1i1p1.latest.zostoga',
          'cmip5.output1.BCC.bcc-csm1-1.rcp45.mon.ocean.Omon.r1i1p1.latest.zostoga',
          'cmip5.output1.MOHC.HadGEM2-ES.rcp45.mon.ocean.Omon.r1i1p1.latest.zostoga',
          'cmip5.output1.CCCma.CanCM4.rcp45.mon.ocean.Omon.r1i1p1.latest.zostoga',
          'cmip5.output1.IPSL.IPSL-CM5A-LR.rcp45.mon.ocean.Omon.r1i1p1.latest.zostoga',
          'cmip5.output1.IPSL.IPSL-CM5A-MR.rcp45.mon.ocean.Omon.r1i1p1.latest.zostoga']


def clear_stores():
    fp_dr = _TestFixProposalStore.config['local.base_dir']
    dc_dr = _TestDatasetCharacterStore.config['local.base_dir']
    for dr in [fp_dr, dc_dr]:
        if os.path.isdir(dr):
            shutil.rmtree(dr)


# populate test character store
def populate_dc_store():
    scan.get_dc_store = Mock(return_value=char_store)

    ds_paths = get_dataset_paths('cmip5', ds_ids=ds_ids, paths=options.project_base_dirs['cmip5'])
    for ds_id, ds_path in ds_paths.items():
        scan_dataset('cmip5', ds_id, ds_path, 'full', 'ceda')


def setup_module():
    clear_stores()
    global char_store
    global prop_store

    char_store = _TestDatasetCharacterStore()
    prop_store = _TestFixProposalStore()

    populate_dc_store()


class _TestRankCheck(RankCheck):
    typical_threshold = .4
    atypical_threshold = .15


def test_RankCheck():
    _base_check.get_dc_store = Mock(return_value=char_store)
    x = _TestRankCheck(ds_ids)
    results, atypical_content, typical_content = x.run()
    print('a=', atypical_content)
    assert atypical_content[0]['data.dim_names'] == ["time", "lev"]
    assert atypical_content[0]['data.shape'] == [1140, 1]
    assert typical_content['data.dim_names'] == ["time"]
    assert typical_content['data.shape'] == [3540]


def test_RankCheck_deduce_fix():
    _base_check.get_dc_store = Mock(return_value=char_store)
    x = _TestRankCheck(ds_ids)
    results, atypical_content, typical_content = x.run()
    d = x.deduce_fix(results[atypical_content[0]], atypical_content[0], typical_content)
    assert (d['dataset_id']['ds_id'] ==
            ['cmip5.output1.INM.inmcm4.rcp45.mon.ocean.Omon.r1i1p1.latest.zostoga'])
    assert (d['fix']['fix_id']) == 'SqueezeDimensionsFix'
    assert (d['fix']['category']) == 'coord_fixes'
    assert (d['fix']['operands']) == {'dims': ['lev']}


class _TestRankCheck1(RankCheck):
    typical_threshold = .7
    atypical_threshold = .3


def test_with_different_thresholds():
    _base_check.get_dc_store = Mock(return_value=char_store)
    x = _TestRankCheck1(ds_ids)
    res = x.run()
    assert res is False


def teardown_module():
    clear_stores()
    