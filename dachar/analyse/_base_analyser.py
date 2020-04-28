from dachar.utils import UNDEFINED


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



