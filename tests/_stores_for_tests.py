from dachar import (
    LocalFixProposalStore,
    LocalFixStore,
    LocalDatasetCharacterStore,
    LocalAnalysisRecordsStore,
)


class _TestDatasetCharacterStore(LocalDatasetCharacterStore):

    store_name = "TestDatasetCharacterStore"
    config = {
        "store_type": "local",
        "local.base_dir": "/tmp/test-ds-char-store",
        "local.dir_grouping_level": 4,
    }


class _TestFixProposalStore(LocalFixProposalStore):

    store_name = "TestFixProposalStore"
    config = {
        "store_type": "local",
        "local.base_dir": "/tmp/test-fix-proposal-store",
        "local.dir_grouping_level": 4,
    }


class _TestFixStore(LocalFixStore):

    store_name = "TestFixStore"
    config = {
        "store_type": "local",
        "local.base_dir": "/tmp/test-fix-store",
        "local.dir_grouping_level": 4,
    }


class _TestAnalysisStore(LocalAnalysisRecordsStore):

    store_name = "TestAnalysisResultsStore"
    config = {
        "store_type": "local",
        "local.base_dir": "/tmp/test-analysis-store",
        "local.dir_grouping_level": 4,
    }
