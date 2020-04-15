from dachar.utils.json_store import _BaseJsonStore


class AnalysisResultsStore(_BaseJsonStore):
    """
    Analysis Results Json Store: A JSON store to hold the results from the analysis of
    populations of ESGF Datasets.
    """

    store_name = 'Analysis Results Store'
    config = {'store_type': 'local',
              'local.base_dir': '/tmp/an-res-store',
              'local.dir_grouping_level': 4}
    id_mappers = {'*': '__ALL__'}
    required_fields = ['dataset_ids', 'analysis_metadata', 'checks', 'results', 'summary',
                       'checks.check_id', 'checks.result.details',
                       'checks.proposed_fix.fix_id', 'checks.proposed_fix.dataset_id',
                       'checks.proposed_fix.operands', 'summary.fixes',
                       'summary.fixes.fix_id', 'summary.fixes.dataset_ids', 'summary.fixes.operands']
    search_defaults = []


ar_store = AnalysisResultsStore()


