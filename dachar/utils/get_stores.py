from dachar.scan.char_store import (
    LocalDatasetCharacterStore,
    ElasticDatasetCharacterStore,
)
from dachar.fixes.fix_proposal_store import (
    LocalFixProposalStore,
    ElasticFixProposalStore,
)
from dachar.analyse.analysis_store import (
    LocalAnalysisRecordsStore,
    ElasticAnalysisRecordsStore,
)
from dachar.fixes.fix_store import LocalFixStore, ElasticFixStore


fix_store = None
ar_store = None
dc_store = None
fix_prop_store = None


def get_fix_store(type=None):
    global fix_store
    if fix_store is None:
        if type == "elasticsearch":
            fix_store = ElasticFixStore()
        else:
            fix_store = LocalFixStore()
    return fix_store


def get_ar_store(type=None):
    global ar_store
    if ar_store is None:
        if type == "elasticsearch":
            ar_store = ElasticAnalysisRecordsStore()
        else:
            ar_store = LocalAnalysisRecordsStore()
    return ar_store


def get_dc_store(type=None):
    global dc_store
    if dc_store is None:
        if type == "elasticsearch":
            dc_store = ElasticDatasetCharacterStore()
        else:
            dc_store = LocalDatasetCharacterStore()
    return dc_store


def get_fix_prop_store(type=None):
    global fix_prop_store
    if fix_prop_store is None:
        if type == "elasticsearch":
            fix_prop_store = ElasticFixProposalStore()
        else:
            fix_prop_store = LocalFixProposalStore()
    return fix_prop_store
