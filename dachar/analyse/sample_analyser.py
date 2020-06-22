from dachar.utils.get_stores import get_ar_store, get_dc_store, get_fix_prop_store
from dachar.utils.options import get_checks
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


class AnalysisRecord(object):
    """
    Provides structure for analysis report object
    """

    def __init__(self, sample_id, ds_ids, location, checks):
        self.record = {
            'sample_id': sample_id,
            'dataset_ids': ds_ids,
            'checks': checks,
            'proposed_fixes': [],
            'analysis_metadata': {
                'location': location,
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


class OneSampleAnalyser(object):
    """
    Takes a sample id and project
    Runs checks on the sample - checks vary per project (cmip5, cmip6, cordex)
    Proposes fixes based on checks run
    """

    def __init__(self, sample_id, project, location, force=False):
        self.sample_id = sample_id
        self.project = project
        self.force = force
        self.location = location

    def _load_ids(self):
        """ Gets list of possible ds_ids from sample_id"""

        base_dir = options.project_base_dirs[self.project]
        _sample_id = os.path.join(base_dir, '/'.join(self.sample_id.split('.')))

        self._sample = []
        for path in glob.glob(_sample_id):
            if self.project in ['cmip5', 'cmip6', 'cordex']:
                self._sample.append('.'.join(path.split('/')[4:]))
            else:
                self._sample.append('.'.join(path.split('/')[5:]))

        return self._sample

    def _characterised(self):
        """ Checks whether ds_ids in sample have been characterised.
        Gets character files from the store or raises and exception
        if some haven't been characterised """

        sample_ids = self._load_ids()
        missing = []
        sample = []

        for ds_id in sample_ids:
            if not get_dc_store().exists(ds_id):
                missing.append(ds_id)
            else:
                sample.append(ds_id)

        if missing:
            raise Exception(f'Some data sets not characterised for sample: {missing}')

    def _analysed(self):
        """
        checks whether already analysed if not - if analysed and force =False then stop.
        If analysed and force = True then carry on. Print statements to say what is happening
        :return:
        """
        if get_ar_store().exists(self.sample_id) and self.force is True:
            print(f'Overwriting existing analysis for {self.sample_id}.')
        elif get_ar_store().exists(self.sample_id) and self.force is False:
            raise Exception(f'Analysis already run for {self.sample_id}. '
                            f'Use force=True to overwrite.')

    def run_check(self, check):
        """ runs each check and returns any proposed fixes"""

        check = check(self._sample)
        run = check.run()
        dict_list = []
        if run:
            results, atypical_content, typical_content = run
            for atypical in atypical_content:
                for ds_id in results[atypical]:
                    d = check.deduce_fix(ds_id, atypical, typical_content)
                    if d:
                        for fix_dict in d:
                            dict_list.append(fix_dict)
            return dict_list
        else:
            return False

    def analyse(self):
        """
        Analyse runs checks, proposes fixes to fix proposal store.
        Also puts a record in analysis record store.
        :return:
        """
        # check if analysed and characterised
        self._characterised()
        self._analysed()

        # get ds_ids in sample and get list of checks to run
        checks = get_checks(self.project)

        # Create analysis record
        a_record = AnalysisRecord(self.sample_id, self._sample, self.location, checks)

        results = {}

        for check in checks:
            check_cls = locate(f'dachar.analyse.checks.{check}')
            result = self.run_check(check_cls)
            if result:
                for d in result:
                    results[check] = d
            else:
                pass

        for check in results:
            fix_dict = results.get(check)
            a_record.add_fix(fix_dict)
            get_fix_prop_store().propose(fix_dict['dataset_id']['ds_id'], fix_dict['fix'])

        get_ar_store().put(self.sample_id, a_record.content, force=self.force)

        print(f'[INFO] Analysis complete for sample: {self.sample_id}')


def analyse(project, sample_id, location, force):
    analysis = OneSampleAnalyser(sample_id, project, location, force)
    analysis.analyse()


class AnalyseMany(object):
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




# write function to create sample ids from cli and use AnalyseMany to run analysis
# AnalyseMany uses OneSampleAnalyser
