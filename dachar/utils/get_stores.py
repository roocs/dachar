from dachar.scan.char_store import DatasetCharacterStore
from dachar.fixes.fix_proposal_store import FixProposalStore
from dachar.analyse.analysis_store import AnalysisRecordsStore
from dachar.fixes.fix_store import FixStore, FixStoreElastic


fix_store = None
ar_store = None
dc_store = None
fix_prop_store = None


def get_fix_store(type=None):
    global fix_store
    if fix_store is None:
        if type == 'elasticsearch':
            fix_store = FixStoreElastic()
        else:
            fix_store = FixStore()    
    return fix_store


def get_ar_store(type=None):
    global ar_store
    if ar_store is None:
        if type == 'elasticsearch':
            ar_store = AnalysisRecordsStoreElastic()
        else:
            ar_store = AnalysisRecordsStore()
    return ar_store


def get_dc_store(type=None):
    global dc_store
    if dc_store is None:
        if type == 'elasticsearch':
            dc_store = DatasetCharacterStoreElastic()
        else:
            dc_store = DatasetCharacterStore()
    return dc_store


def get_fix_prop_store(type=None):
    global fix_prop_store
    if fix_prop_store is None:
        if type == 'elasticsearch':
            fix_prop_store = FixProposalStoreElastic()
        else:
            fix_prop_store = FixProposalStore()
    return fix_prop_store
