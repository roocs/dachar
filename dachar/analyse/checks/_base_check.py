import logging
import pprint as pp

from dachar.utils import UNDEFINED, nested_lookup, JDict

from dachar import fix_proposal_store, dc_store

from dachar.fixes.fix_api import get_fix

logging.basicConfig()
log = logging.getLogger(__name__)


# AGREED PLAN
"""

1. Fix Store is only the published fixes.
2. Withdrawn fixes are recorded in change log.
3. Fix Proposal Store holds the status of each fix.
4. In the Fix Proposal Store:
 - ds_id
   fixes:
    fix:
      fix_id
      operands
    reason
    status
    timestamp
    history:
      [{status, reason, timestamp},
       {status, reason, timestamp}]

5. Make sure it logs to history
"""

#TODO: Should we send in pre-loaded cache object of all the dc_store records
#      - then each check uses them directly.


class _BaseCheck(object):

    # Required class attributes:
    # - characteristics: list of characteristics to compare
    # - associated_fix:  identifier of fix associated with this check
    # - typical_threshold:  fraction of data sets that must contain common characteristics
    #                       in order to identify "typical" (common) values
    # - atypical_threshold: fraction of data sets beneath which the found characteristics
    #                       should be treated as "atypical"; in which case a "fix" will be suggested
    characteristics = UNDEFINED
    associated_fix = UNDEFINED

    typical_threshold = .8
    atypical_threshold = .2

    def __init__(self, sample):
        self.sample = sample
        self._load()

    def _load(self):
        # Checks sample has been characterised
        self._cache = {}
        missing = []

        for ds_id in self.sample:
            if not dc_store.exists(ds_id):
                missing.append(ds_id)
            else:
                self._cache[ds_id] = dc_store.get(ds_id)

        if missing:
            raise Exception(f'Some data sets not characterised for sample: {missing}')

    def run(self):
        content = self._extract_content()
        # Create a dictionary that can
        results = JDict()

        for ds_id, items in content:
            results.setdefault(items, [])
            results[items].append(ds_id)

        total = len(content)

#       print(f'\n[INFO] Testing: {keys} - found {len(results)} varieties')
        typical_content = None
        atypical_content = []

        # fake_results = {'test1': ['1.1.1.1.1'],
        #                 'test2': ['1.1.1.1.1', '2.1.1.1.1']}

        # Count different values found and convert to fractions of total
        for key in results.keys():

            ds_ids = results[key]
            fraction = len(ds_ids) / total

            if fraction >= self.typical_threshold:
                typical_content = key

            if fraction <= self.atypical_threshold:
                atypical_content.append(key)

        # We now have:
        # if a value occurs more than the typical threshold:     set as typical
        # if any value occurs less than the atypical threshold:  append to the atypical list (to fix)

        # Suggest fixes for any values that are atypical but ONLY do so if typical values are found
        if typical_content is not None:

            for atypical in atypical_content:

                for ds_id in results[atypical]:
                    return ds_id, atypical, typical_content
                    #self._process_fix(ds_id, atypical, typical_content)

        else:
            return False

    def _extract_content(self):
        content = []

        for ds_id in self.sample:
            items = dict([(key, nested_lookup(key, self._cache[ds_id], must_exist=True))
                          for key in self.characteristics])
            content.append((ds_id, items))

        return content

    def _process_fix(self, ds_id, atypical_content, typical_content):
        fix = self.deduce_fix(atypical_content, typical_content)
        self._propose_fix(ds_id, fix)

    def deduce_fix(self, ds_id, atypical_content, typical_content):
        # Compare two dictionaries to work out what the difference is
        # Return a Fix based on that difference
        raise NotImplementedError

    def _propose_fix(self, ds_id, fix):
        fix_proposal_store.propose(ds_id, fix)



