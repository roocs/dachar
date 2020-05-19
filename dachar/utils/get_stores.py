from dachar.scan.char_store import DatasetCharacterStore
from dachar.fixes.fix_proposal_store import FixProposalStore
from dachar.analyse.analysis_store import AnalysisRecordsStore
from dachar.fixes.fix_store import FixStore


fix_store = None
ar_store = None
dc_store = None
fix_prop_store = None


def get_fix_store():
    global fix_store
    if fix_store is None:
        fix_store = FixStore()
    return fix_store


def get_ar_store():
    global ar_store
    if ar_store is None:
        ar_store = AnalysisRecordsStore()
    return ar_store


def get_dc_store():
    global dc_store
    if dc_store is None:
        dc_store = DatasetCharacterStore()
    return dc_store


def get_fix_prop_store():
    global fix_prop_store
    if fix_prop_store is None:
        fix_prop_store = FixProposalStore()
    return fix_prop_store
