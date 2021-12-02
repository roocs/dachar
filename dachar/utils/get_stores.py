from dachar.analyse.analysis_store import ElasticAnalysisRecordsStore
from dachar.analyse.analysis_store import LocalAnalysisRecordsStore
from dachar.fixes.fix_proposal_store import ElasticFixProposalStore
from dachar.fixes.fix_proposal_store import LocalFixProposalStore
from dachar.fixes.fix_store import ElasticFixStore
from dachar.fixes.fix_store import LocalFixStore
from dachar.scan.char_store import ElasticDatasetCharacterStore
from dachar.scan.char_store import LocalDatasetCharacterStore
from dachar import CONFIG

DEFAULT_STORE_TYPE = CONFIG.get("dachar:store", {}).get("store_type", "local")

fix_store = None
ar_store = None
dc_store = None
fix_prop_store = None


def get_fix_store(type=DEFAULT_STORE_TYPE):
    global fix_store
    if fix_store is None:
        if type == "elasticsearch":
            fix_store = ElasticFixStore()
        else:
            fix_store = LocalFixStore()
    return fix_store


def get_ar_store(type=DEFAULT_STORE_TYPE):
    global ar_store
    if ar_store is None:
        if type == "elasticsearch":
            ar_store = ElasticAnalysisRecordsStore()
        else:
            ar_store = LocalAnalysisRecordsStore()
    return ar_store


def get_dc_store(type=DEFAULT_STORE_TYPE):
    global dc_store
    if dc_store is None:
        if type == "elasticsearch":
            dc_store = ElasticDatasetCharacterStore()
        else:
            dc_store = LocalDatasetCharacterStore()
    return dc_store


def get_fix_prop_store(type=DEFAULT_STORE_TYPE):
    global fix_prop_store
    if fix_prop_store is None:
        if type == "elasticsearch":
            fix_prop_store = ElasticFixProposalStore()
        else:
            fix_prop_store = LocalFixProposalStore()
    return fix_prop_store


def get_store_by_name(name):
    if name == "fix":
        return get_fix_store()

    elif name == "fix-proposal":
        return get_fix_prop_store()

    elif name == "analysis":
        return get_ar_store()

    elif name == "character":
        return get_dc_store()

    else:
        raise Exception(
            f"Invalid store: {name}. Expected one of fix, fix-proposal, character or analysis"
        )
