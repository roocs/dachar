import os
import shutil
import glob

from tests._stores_for_tests import _TestFixProposalStore, _TestAnalysisStore, _TestDatasetCharacterStore
from dachar.utils import options
from dachar.scan.scan import scan_dataset, get_dataset_paths
from dachar.analyse import OneSampleAnalyser
from mockito import mock, when

# how to use real class and change stores used??

char_store = None
prop_store = None
analysis_store = None

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
    ar_dr = _TestAnalysisStore.config['local.base_dir']
    dc_dr = _TestDatasetCharacterStore.config['local.base_dir']
    for dr in [fp_dr, ar_dr, dc_dr]:
        if os.path.isdir(dr):
            shutil.rmtree(dr)


def setup_module():
    clear_stores()
    global char_store
    global prop_store
    global analysis_store

    char_store = _TestDatasetCharacterStore()
    prop_store = _TestFixProposalStore()
    analysis_store = _TestAnalysisStore()


class _TestOneSampleAnalyser(OneSampleAnalyser):

    def _load_ids(self):
        """ Gets list of possible ds_ids from sample_id"""

        base_dir = options.project_base_dirs[self.project]
        _sample_id = os.path.join(base_dir, '/'.join(self.sample_id.split('.')))

        self._sample = []
        for path in glob.glob(_sample_id):
            if self.project in ['cmip5', 'cmip6', 'cordex']:
                self._sample.append('.'.join(path.split('/')[6:]))
            else:
                self._sample.append('.'.join(path.split('/')[7:]))

        return self._sample


# populate test character store
def populate_dc_store():
    ds_paths = get_dataset_paths('cmip5', ds_ids=ds_ids, paths=options.project_base_dirs['cmip5'])
    for ds_id, ds_path in ds_paths.items():
        scan_dataset('cmip5', ds_id, ds_path, 'full', char_store, 'ceda')


def test_analyse():
    populate_dc_store()
    zostoga_sample_id = "cmip5.output1.*.*.rcp45.mon.ocean.Omon.r1i1p1.latest.zostoga"
    zostoga = _TestOneSampleAnalyser(zostoga_sample_id, 'cmip5', 'ceda', char_store, analysis_store,
                                     prop_store, force=True)

    zostoga.analyse()


def teardown_module():
    clear_stores()
