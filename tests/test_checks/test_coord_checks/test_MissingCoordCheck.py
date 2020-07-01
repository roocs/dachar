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

options.project_base_dirs['cmip6'] = \
     'tests/mini-esgf-data/test_data/badc/cmip6/data'
options.project_base_dirs['cmip5'] = \
     'tests/mini-esgf-data/test_data/badc/cmip5/data'

ds_ids_cmip6 = ['CMIP6.CMIP.NCAR.CESM2.historical.r1i1p1f1.SImon.siconc.gn.latest',
                'CMIP6.CMIP.SNU.SAM0-UNICON.historical.r1i1p1f1.SImon.siconc.gn.latest',
                'CMIP6.CMIP.CSIRO.ACCESS-ESM1-5.historical.r1i1p1f1.SImon.siconc.gn.latest',
                'CMIP6.CMIP.CCCma.CanESM5.historical.r1i1p1f1.SImon.siconc.gn.latest',
                'CMIP6.CMIP.MPI-M.MPI-ESM1-2-HR.historical.r1i1p1f1.SImon.siconc.gn.latest']
# 'CMIP6.CMIP.BCC.BCC-ESM1.historical.r1i1p1f1.SImon.siconc.gn.latest']
# 'CMIP6.CMIP.MIROC.MIROC6.historical.r1i1p1f1.SImon.siconc.gn.latest',]
# 'CMIP6.CMIP.IPSL.IPSL-CM6A-LR.historical.r1i1p1f1.SImon.siconc.gn.latest',
# 'CMIP6.CMIP.NOAA-GFDL.GFDL-ESM4.historical.r1i1p1f1.SImon.siconc.gn.latest'

ds_ids_cmip5 = ['cmip5.output1.ICHEC.EC-EARTH.historical.mon.atmos.Amon.r1i1p1.latest.tas',
          'cmip5.output1.MOHC.HadGEM2-ES.historical.mon.atmos.Amon.r1i1p1.latest.tas',
          'cmip5.output1.IPSL.IPSL-CM5A-LR.historical.mon.atmos.Amon.r1i1p1.latest.tas',
          'cmip5.output1.INM.inmcm4.historical.mon.atmos.Amon.r1i1p1.latest.tas',
          'cmip5.output1.NCAR.CCSM4.historical.mon.atmos.Amon.r1i1p1.latest.tas']


def clear_stores():
    fp_dr = _TestFixProposalStore.config['local.base_dir']
    dc_dr = _TestDatasetCharacterStore.config['local.base_dir']
    for dr in [fp_dr, dc_dr]:
        if os.path.isdir(dr):
            shutil.rmtree(dr)


# populate test character store
def populate_dc_store(ds_ids, project):
    scan.get_dc_store = Mock(return_value=char_store)

    ds_paths = get_dataset_paths(project, ds_ids=ds_ids, paths=options.project_base_dirs[project])
    for ds_id, ds_path in ds_paths.items():
        scan_dataset(project, ds_id, ds_path, 'full', 'ceda')


def setup_module():
    clear_stores()
    global char_store
    global prop_store

    char_store = _TestDatasetCharacterStore()
    prop_store = _TestFixProposalStore()

    populate_dc_store(ds_ids_cmip6, 'cmip6')
    populate_dc_store(ds_ids_cmip5, 'cmip5')


class _TestMissingCoordCheck(MissingCoordCheck):
    typical_threshold = .8
    atypical_threshold = .2


def test_MissingCoordCheck_cmip6():
    _base_check.get_dc_store = Mock(return_value=char_store)
    x = _TestMissingCoordCheck(ds_ids_cmip6)
    results, atypical_content, typical_content = x.run()
    assert atypical_content[0]['coordinates.*.id'] == ['latitude', 'longitude', 'ni', 'nj', 'time']
    assert typical_content['coordinates.*.id'] == ['i', 'j', 'latitude', 'longitude', 'time', 'type']


def test_MissingCoordCheck_deduce_fix_cmip6():
    _base_check.get_dc_store = Mock(return_value=char_store)
    x = _TestMissingCoordCheck(ds_ids_cmip6)
    results, atypical_content, typical_content = x.run()
    print(results, atypical_content, typical_content)
    d = x.deduce_fix(results[atypical_content[0]], atypical_content[0], typical_content)
    assert (d[0]['dataset_id']['ds_id'] ==
            ['CMIP6.CMIP.NCAR.CESM2.historical.r1i1p1f1.SImon.siconc.gn.latest'])
    assert (d[0]['fix']['fix_id']) == 'AddScalarCoordFix'
    assert (d[0]['fix']['category']) == 'coord_fixes'
    assert (d[0]['fix']['operands']) == {'dtype': '|S7',
                                         'id': 'type',
                                         'value': 'sea_ice',
                                         'length': 1,
                                         'attrs':
                                          {'long_name': 'Sea Ice area type',
                                           'standard_name': 'area_type'}}




def test_MissingCoordCheck_cmip5():
    _base_check.get_dc_store = Mock(return_value=char_store)
    x = _TestMissingCoordCheck(ds_ids_cmip5)
    results, atypical_content, typical_content = x.run()
    assert atypical_content[0]['coordinates.*.id'] == ['latitude', 'longitude', 'time']
    assert typical_content['coordinates.*.id'] == ['height', 'latitude', 'longitude', 'time']


def test_MissingCoordCheck_deduce_fix_cmip5():
    _base_check.get_dc_store = Mock(return_value=char_store)
    x = _TestMissingCoordCheck(ds_ids_cmip5)
    results, atypical_content, typical_content = x.run()
    d = x.deduce_fix(results[atypical_content[0]], atypical_content[0], typical_content)
    assert (d[0]['dataset_id']['ds_id'] ==
            ['cmip5.output1.ICHEC.EC-EARTH.historical.mon.atmos.Amon.r1i1p1.latest.tas'])
    assert (d[0]['fix']['fix_id']) == 'AddScalarCoordFix'
    assert (d[0]['fix']['category']) == 'coord_fixes'
    assert (d[0]['fix']['operands']) == {'dtype': 'float64',
                                      'value': 2.0, 
                                      'id': 'height', 
                                      'length': 1, 
                                      'attrs': 
                                          {'axis': 'Z', 
                                           'long_name': 'height', 
                                           'positive': 'up', 
                                           'standard_name': 'height', 
                                           'units': 'm'}
                                      }


class _TestMissingCoordCheck1(MissingCoordCheck):
    typical_threshold = .90
    atypical_threshold = .10


def test_with_different_thresholds_cmip6():
    _base_check.get_dc_store = Mock(return_value=char_store)
    x = _TestMissingCoordCheck1(ds_ids_cmip5)
    res = x.run()
    assert res is False


def test_with_different_thresholds_cmip5():
    _base_check.get_dc_store = Mock(return_value=char_store)
    x = _TestMissingCoordCheck1(ds_ids_cmip5)
    res = x.run()
    assert res is False


def teardown_module():
    # clear_stores()
    pass


# need a test that checks when there are 2 scalar coordinates missing