from dachar.analyse.checks.coord_checks import *


from tests._stores_for_tests import _TestDatasetCharacterStore, \
    _TestFixProposalStore, _TestFixStore


char_store = None
prop_store = None


def setup_module():
    # Populate a set of checks in a test Character Store
    # Modify the test Character Store to use a test Proposal Store
    global char_store
    global prop_store
    char_store = _TestDatasetCharacterStore()
    prop_store = _TestFixProposalStore()


def test_RankCheck():
    x = RankCheck([ds1, ds2, ds3])
    x.run()


class _TestRankCheck(RankCheck):
    def __init__(self, sample):
        pass


def test_RankCheck_deduce_fix():

    x = RankCheck([ds1, ds2, ds3])
    typical = {'shape': [1,2]}
    deduced = x._deduce_fix()


