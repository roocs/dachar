from dachar.scan.char_store import DatasetCharacterStore
from dachar.fixes.fix_proposal_store import FixProposalStore
from dachar.analyse.analysis_store import AnalysisRecordsStore
from dachar.fixes.fix_store import FixStore


def get_fix_store():
    fix_store = FixStore()
    return fix_store


def get_ar_store():
    ar_store = AnalysisRecordsStore()
    return ar_store


def get_dc_store():
    dc_store = DatasetCharacterStore()
    return dc_store


def get_fix_prop_store():
    fix_prop_store = FixProposalStore()
    return fix_prop_store
