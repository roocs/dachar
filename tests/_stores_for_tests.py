from dachar import FixProposalStore, FixStore, DatasetCharacterStore, AnalysisRecordsStore


class _TestDatasetCharacterStore(DatasetCharacterStore):

    store_name = 'TestDatasetCharacterStore'
    config = {'store_type': 'local',
              'local.base_dir': '/tmp/ds-char-store',
              'local.dir_grouping_level': 4}


class _TestFixProposalStore(FixProposalStore):

    store_name = 'TestFixProposalStore'
    config = {'store_type': 'local',
              'local.base_dir': '/tmp/test-fix-proposal-store',
              'local.dir_grouping_level': 4}


class _TestFixStore(FixStore):

    store_name = 'TestFixStore'
    config = {'store_type': 'local',
              'local.base_dir': '/tmp/test-fix-store',
              'local.dir_grouping_level': 4}


class _TestAnalysisStore(AnalysisRecordsStore):

    store_name = 'TestAnalysisResultsStore'
    config = {'store_type': 'local',
              'local.base_dir': '/tmp/test-analysis-store',
              'local.dir_grouping_level': 4}

