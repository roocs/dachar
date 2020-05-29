import json
import os


class _BaseCheck(object):
    pass


class RankCheck(_BaseCheck):
    def __init__(self):
        pass

    def run(self):
        pass

    def save_result(self):
        pass

    def suggest_fixes(self):
        pass

    def suggest_fix(self):
        pass

    def write_fixes(self):
        pass

    def write_fix(self):
        pass


class GrandAnalyser(object):
    def __init__(self, project):
        self._project = project
        self.analyse_all()

    def analyse_all(self):
        for population in self._get_populations():
            self.analyse(population)

    def analyse(self, population):
        pass

    # Use a generator
    def _get_populations(self):
        for i in range(1000):
            yield i


# Is the check store a superset of the fixes?


def prep_dir(dr):
    if not os.path.isdir(dr):
        os.makedirs(dr)


class JsonStore(object):

    SPLIT_LEVEL = 0

    def __init__(self, location):
        self._location = location
        self._setup()

    def setup(self):
        prep_dir(self._location)

    def put(self, id, content):
        pth = self._id_to_path(id)

        with open(pth, "w") as writer:
            json.dump(content, writer)

    def search(self, terms=None, freetext=None):
        pass

    def get(self, id):
        return

    def _id_to_path(self, id):
        comps = id.split(".", self.SPLIT_LEVEL)
        fname = comps[-1] + ".json"
        return os.path.join(self._location, *comps[:-1], fname)


class CheckStore(object):
    def __init__(self):
        pass

    def get(self):
        pass

    def put(self):
        pass

    def update(self):
        pass

    def search(self, result):
        pass


class PopulationBuilder(object):
    def __init__(self, project):
        self._project = project

    def _build_populations(self):
        pass


"""
Class RankCheck(_BaseCheck):

Init
Run
Save result
Suggest fixes
Suggest fix
Create fixes
Create fix

Analyse all cmip5
Identify populations cmip5
Analyse population cmip5 slice

Class CheckStore

Init
Get
Put
Update id check
Search by check result - get suggested fix

How to identify populations?
Should they have an identifier with an asterisk in?
Is that how you look up checks in the check store?

Is the check store a superset of the fixes?

"""
