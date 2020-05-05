import os
import shutil
import glob
from pydoc import locate
import datetime

from tests._stores_for_tests import _TestFixProposalStore, _TestAnalysisStore, _TestDatasetCharacterStore
from dachar.utils import options
from dachar.scan.scan import scan_dataset, get_dataset_paths
from dachar.utils.options import get_checks
from dachar import __version__ as version
from dachar.analyse.checks.coord_checks import RankCheck


char_store = None
prop_store = None
analysis_store = None

options.project_base_dirs['cmip5'] = \
    'tests/mini-esgf-data/test_data/badc/cmip5/data'

ds_ids = ['cmip5.output1.INM.inmcm4.rcp45.mon.ocean.Omon.r1i1p1.latest.zostoga',
          'cmip5.output1.MPI-M.MPI-ESM-LR.rcp45.mon.ocean.Omon.r1i1p1.latest.zostoga',
          'cmip5.output1.MOHC.HadGEM2-ES.rcp45.mon.ocean.Omon.r1i1p1.latest.zostoga']


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


class AnalysisReport(object):
    """
    Provides structure for analysis report object
    """

    def __init__(self, sample_id, ds_ids, checks):
        self.record = {
            'sample_id': sample_id,
            'dataset_ids': ds_ids,
            'checks': checks,
            'proposed_fixes': [],
            'analysis_metadata': {
                'location': 'ceda',
                'datetime': (datetime.datetime.now()).strftime('%d/%m/%Y, %H:%M'),
                'software_version': version
            }
        }

    def add_fix(self, fix):
        fixes = self.record.get('proposed_fixes', [])
        fixes.append(fix)
        self.record['proposed_fixes'] = fixes

    @property
    def content(self):
        return self.record


class FakeOneSampleAnalyser(object):

    def __init__(self, sample_id, project, force=False):
        self.sample_id = sample_id
        self.project = project
        self.force = force

    def _load_ids(self):

        base_dir = options.project_base_dirs[self.project]
        _sample_id = os.path.join(base_dir, '/'.join(self.sample_id.split('.')))

        self._sample = []
        for path in glob.glob(_sample_id):
            self._sample.append('.'.join(path.split('/')[6:]))

        return self._sample

    def _characterised(self):

        sample_ids = self._load_ids()
        missing = []
        sample = []

        for ds_id in sample_ids:
            if not char_store.exists(ds_id):
                missing.append(ds_id)
            else:
                sample.append(ds_id)

        if missing:
            raise Exception(f'Some data sets not characterised for sample: {missing}')

    def _analysed(self):

        if analysis_store.exists(self.sample_id) and self.force is True:
            print(f'Overwriting existing analysis for {self.sample_id}.')
        elif analysis_store.exists(self.sample_id) and self.force is False:
            raise Exception(f'Analysis already run for {self.sample_id}. '
                            f'Use force=True to overwrite.')

    def run_check(self, check):

        check = check(self._sample)
        run = check.run()
        if run:
            ds_id, atypical, typical_content = run
            d = check.deduce_fix(ds_id, atypical, typical_content)
            return d
        else:
            return False

    def analyse(self):

        # check if analysed and characterised
        self._characterised()
        self._analysed()

        # get ds_ids in sample and get list of checks to run
        checks = get_checks(self.project)

        # Create analysis record
        a_record = AnalysisReport(self.sample_id, self._sample, checks)

        results = {}

        for check in checks:
            check_cls = locate(f'dachar.analyse.checks.{check}')
            result = self.run_check(check_cls)
            if result:
                results[check] = result
            else:
                pass

        for check in results:
            fix_dict = results.get(check)
            a_record.add_fix(fix_dict)
            prop_store.propose(fix_dict['dataset_id']['ds_id'], fix_dict['fix'])

        analysis_store.put(self.sample_id, a_record.content, force=self.force)

        print(f'[INFO] Analysis complete for sample:{self.sample_id}')


# populate test character store
def populate_dc_store():
    ds_paths = get_dataset_paths('cmip5', ds_ids=ds_ids, paths=options.project_base_dirs['cmip5'])
    for ds_id, ds_path in ds_paths.items():
        character, ds_id = scan_dataset('cmip5', ds_id, ds_path, 'full', 'ceda')
        char_store.put(ds_id, character, force=True)


def test_analyse():
    populate_dc_store()
    zostoga_sample_id = "cmip5.output1.*.*.rcp45.mon.ocean.Omon.r1i1p1.latest.zostoga"
    zostoga = FakeOneSampleAnalyser(zostoga_sample_id, 'cmip5', force=True)
    zostoga.analyse()


def teardown_module():
    clear_stores()
