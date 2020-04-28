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
    required_fields = ['sample_id', 'dataset_ids', 'checks', 'fixes', 'analysis_metadata']
    search_defaults = []


import datetime

eg_record = {
    'sample_id': 'cmip5.*',
    'dataset_ids': ['cmip5.tas', 'cmip5.pr'],
    'checks': ['RankCheck', 'OutlierRangeCheck', 'OtherCheck'],
    'fixes': [
        {
            'fix_id': 'RankFix',
            'dataset_id': 'cmip5.pr',
            'operands': {
                'rank': 2
            },
            'status': 'proposed'
        },
        {
            'fix_id': 'OtherCheck',
            'dataset_id': 'cmip5.tas',
            'operands': {},
            'status': 'proposed'
        },
        {
            'fix_id': 'OtherCheck',
            'dataset_id': 'cmip5.pr',
            'operands': {},
            'status': 'proposed'
        },
    ],
    'analysis_metadata': {
        'location': 'ceda',
        'datetime': datetime.datetime.now()
    }
}


