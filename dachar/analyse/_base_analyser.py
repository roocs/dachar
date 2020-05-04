from dachar.utils import UNDEFINED
from dachar.fixes._base_fix import FixDetails
from dachar import dc_store, fix_proposal_store, ar_store
from dachar.utils.options import get_checks
from dachar.analyse.checks.coord_checks import RankCheck
from dachar.utils import options
from dachar import __version__ as version


import os
import datetime
import glob
from pydoc import locate

"""
1. Per project, can we run a massive "analyse all" job.
2. We need to know what each sample looks like.
 - see: https://github.com/roocs/dachar/issues/37
3. Need to generate each sample id based on rules.
4. We need an "analyse one sample" workflow manager - class.
  - for each check:
    - run check:
      - propose fixes if required
  - log all results to Json Store
"""

"""
Separately:
1. Review proposed checks
2. Test
3. Publish OR Reject checks
  - which automatically updates the Fix Store.
"""


class SampleBuilder(object):
    """
    Build each sample id based on rules
    Will generate samples from cli options
    """
    def __init__(self, project):
        self._project = project

    def _build_samples(self):
        return "cmip5.output1.MOHC.HadGEM2-ES.historical.mon.land.Lmon.*.latest.rh"


class AnalysisReport(object):
    """
    Provides structure for analysis report object
    """

    def __init__(self, sample_id, ds_ids, checks):
        self.data = {}
        self.record = {
            'sample_id': sample_id,
            'dataset_ids': ds_ids,
            'checks': checks,
            'proposed_fixes': [],
            'analysis_metadata': {
                'location': 'ceda',
                'datetime': datetime.datetime.now(),
                'software_version': version
            }
        }

    # @property
    # def proposed_fixes(self):
    #     return self.data['proposed_fixes']

    def add_fix(self, fix):
        fixes = self.data.get('proposed_fixes', [])
        fixes.append(fix)
        self.data['proposed_fixes'] = fixes


# class FixProposal(object):
#     """
#     structure of record
#         {'dataset_id': 'ds.1.1.1.1.1.1',
#          'fixes': [{'fix': {'fix_id': 'fix_id',
#                             'title': 'title',
#                             'description': 'description',
#                             'category': 'category',
#                             'reference_implementation': 'ref_implementation',
#                             'operands': 'operands'},
#                     'history': [],
#                     'reason': '',
#                     'status': 'proposed',
#                     'timestamp': '2020-04-29T14:41:52'}]}
#     """
#
#     def __init__(self):
#         self.data = {}
#
#     @property
#     def fixes(self):
#         return self.data['fixes']
#
#     def add_fix(self, fix):
#         fixes = self.data.get('fixes', [])
#         fixes.append(fix)
#         self.data['fixes'] = fixes


class OneSampleAnalyser(object):
    """
    Takes a sample id and project
    Runs checks on the sample - checks vary per project (cmip5, cmip6, cordex)
    Proposes fixes based on checks run
    returns results as a dict

    """

    def __init__(self, sample_id, project, force=False):
        self.sample_id = sample_id
        self.project = project
        self.force = force

    def _load_ids(self, sample_id):
        """ Gets list of possible ds_ids from sample_id"""

        base_dir = options.project_base_dirs[self.project]
        sample_id = os.path.join(base_dir, '/'.join(sample_id.split('.')))

        sample = []
        for path in glob.glob(sample_id):
            sample.append('.'.join(path.split('/')[4:]))

        return sample

    def _characterised(self):
        """ Checks whether ds_ids in sample have been characterised.
        Gets character files from the store or raises and exception
        if some haven't been characterised"""

        sample = self._load_ids(self)
        self._cache = {}
        missing = []

        for ds_id in sample:
            if not dc_store.exists(ds_id):
                missing.append(ds_id)
            else:
                self._cache[ds_id] = dc_store.get(ds_id)

        if missing:
            raise Exception(f'Some data sets not characterised for sample: {missing}')

    def _analysed(self):
        """
        checks whether already analysed if not - if analysed and force =False then stop.
        If analysed and force = True then carry on. Print statements to say what is happening
        :return:
        """
        if ar_store.exists(self.sample_id) and self.force is True:
            print(f'Overwriting existing analuysis for {self.sample_id}.')
        elif ar_store.exists(self.sample_id) and self.force is False:
            raise Exception(f'Analysis already run for {self.sample_id}. '
                            f'Use force=True to overwrite.')

    def run_check(self, check, sample):
        """ runs each check and returns any proposed fixes
        What does it run checks on? - all ds_ids in the sample
         needs to get checks"""

        # needs to keep track of fix proposal and return
        # need to create check object using name of check
        check = check(sample)
        run = check.run()
        if run is not None:
            d = check.deduce_fix(run)
            return d

    def analyse(self):
        """
        Analyse runs checks, proposes fixes and
        saves all results in proposed fixes store(?)
        :return:
        """
        # check if analysed and characterised
        self._characterised()
        self._analysed()

        # get ds_ids in sample and get list of checks to run
        sample = self._cache
        checks = get_checks(self.project)

        # Create analysis record
        a_record = AnalysisReport(self.sample_id, sample, checks)

        results = {}

        for check in checks:
            check_cls = locate(f'dachar.analyse.checks.{check}')
            results[check] = self.run_check(check_cls, sample)

        for check in results:
            fix_dict = results.get(check)
            a_record.add_fix(fix_dict)
            fix_proposal_store.propose(fix_dict['dataset_id'], fix_dict['fix'])

        ar_store.put(self.sample_id, a_record, force=self.force)

        # @property
        # def results(self):
        #     return self.results
        print(f'[INFO] Analysis complete for {self.sample_id}')


# not sure abput this one? - could use a function to analyse all samples

class GrandAnalyser(object):
    """
    To run over all samples of a given project?
    """

    def __init__(self):
        self._analyse_all()

    def analyse_all(self):
        for sample in self._get_sample():
            self.analyse(sample)



    # Use a generator
    def _get_sample(self):
        for i in range(1000):
            yield i


if __name__ == '__main__':
    zostoga_sample_id = "cmip5.output1.*.*.rcp45.mon.ocean.Omon.r1i1p1.latest.zostoga"
    zostoga = OneSampleAnalyser(zostoga_sample_id, 'cmip5', force=False)
    zostoga.analyse()
    # Try and get onesampleanalyser working for zostoga example - only check with
    # squeezedims
    # Needs to produce analysis record
    # and propose fixes to fixes store
