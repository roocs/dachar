from dachar.utils import UNDEFINED




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



class _BaseSampleAnalyser(object):

    checks = UNDEFINED

    def __init__(self, project):
        self._project = project
        self.analyse_all()

    def _load(self, sample):
        pass # use json store to load into a list of dicts

    def run(self):
        sample = self._load()
        results = {}

        for check in self.checks:
            results[check] = self.run_check(check, sample)

        return results

    @property
    def results(self):
        return self.results


class GrandAnalyser(object):
#!!! What about project?

    def __init__(self):
        self._analyse_all()

    def analyse_all(self):
        for sample in self._get_sample():
            self.analyse(sample)

    def analyse(self, sample):
        pass

    # Use a generator
    def _get_sample(self):
        for i in range(1000):
            yield i


class SampleBuilder(object):

    def __init__(self, project):
        self._project = project

    def _build_samples(self):
        pass



