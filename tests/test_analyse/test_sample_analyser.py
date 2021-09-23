import glob
import os
import shutil
from unittest.mock import Mock

from roocs_utils.project_utils import get_project_base_dir

from dachar.analyse import OneSampleAnalyser
from dachar.analyse import sample_analyser
from dachar.analyse.checks import _base_check
from dachar.scan import scan
from dachar.scan.scan import get_dataset_paths
from dachar.scan.scan import scan_dataset
from tests._stores_for_tests import _TestAnalysisStore
from tests._stores_for_tests import _TestDatasetCharacterStore
from tests._stores_for_tests import _TestFixProposalStore

char_store = None
prop_store = None
analysis_store = None


ds_ids = [
    "cmip5.output1.INM.inmcm4.rcp45.mon.ocean.Omon.r1i1p1.latest.zostoga",
    "cmip5.output1.MPI-M.MPI-ESM-LR.rcp45.mon.ocean.Omon.r1i1p1.latest.zostoga",
    "cmip5.output1.BCC.bcc-csm1-1.rcp45.mon.ocean.Omon.r1i1p1.latest.zostoga",
    "cmip5.output1.MOHC.HadGEM2-ES.rcp45.mon.ocean.Omon.r1i1p1.latest.zostoga",
    "cmip5.output1.CCCma.CanCM4.rcp45.mon.ocean.Omon.r1i1p1.latest.zostoga",
    "cmip5.output1.IPSL.IPSL-CM5A-LR.rcp45.mon.ocean.Omon.r1i1p1.latest.zostoga",
    "cmip5.output1.IPSL.IPSL-CM5A-MR.rcp45.mon.ocean.Omon.r1i1p1.latest.zostoga",
]


def clear_stores():
    fp_dr = _TestFixProposalStore.config["local.base_dir"]
    ar_dr = _TestAnalysisStore.config["local.base_dir"]
    dc_dr = _TestDatasetCharacterStore.config["local.base_dir"]
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
        base_dir = get_project_base_dir(self.project)
        _sample_id = os.path.join(base_dir, "/".join(self.sample_id.split(".")))

        self._sample = []
        for path in glob.glob(_sample_id):
            self._sample.append(".".join(path.split("/")[-11:]))

        return self._sample


# use mock to change the stores used to the test stores


# populate test character store
def populate_dc_store():
    scan.get_dc_store = Mock(return_value=char_store)

    ds_paths = get_dataset_paths("cmip5", ds_ids=ds_ids)
    for ds_id, ds_path in ds_paths.items():
        scan_dataset("cmip5", ds_id, ds_path, "full", "ceda")


def test_analyse(load_esgf_test_data):
    sample_analyser.get_ar_store = Mock(return_value=analysis_store)
    sample_analyser.get_dc_store = Mock(return_value=char_store)
    sample_analyser.get_fix_prop_store = Mock(return_value=prop_store)
    _base_check.get_dc_store = Mock(return_value=char_store)

    populate_dc_store()

    zostoga_sample_id = "cmip5.output1.*.*.rcp45.mon.ocean.Omon.r1i1p1.latest.zostoga"
    zostoga = _TestOneSampleAnalyser(zostoga_sample_id, "cmip5", "ceda")
    zostoga.analyse()


def teardown_module():
    clear_stores()
