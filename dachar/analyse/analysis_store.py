
from dachar.utils.json_store import _BaseJsonStore


class AnalysisRecordsStore(_BaseJsonStore):
    """
    Analysis Results Json Store: A JSON store to hold the results from the analysis of
    populations of ESGF Datasets.
    """

    store_name = 'Analysis Results Store'
    config = {'store_type': 'local',
              'local.base_dir': '/tmp/an-res-store',
              'local.dir_grouping_level': 4}
    id_mappers = {'*': '__ALL__'}
    required_fields = ['sample_id', 'dataset_ids', 'checks', 'proposed_fixes', 'analysis_metadata']
    search_defaults = []





