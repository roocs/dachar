import datetime

from dachar import __version__ as version
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


eg_record = {
    'sample_id': 'c3s-cordex.output.EUR-11.IPSL.MOHC-HadGEM2-ES.rcp85.r1i1p1.IPSL-WRF381P.v1.day.*.v20190212',
    'dataset_ids': [
        'c3s-cordex.output.EUR-11.IPSL.MOHC-HadGEM2-ES.rcp85.r1i1p1.IPSL-WRF381P.v1.day.tas.v20190212',
        'c3s-cordex.output.EUR-11.IPSL.MOHC-HadGEM2-ES.rcp85.r1i1p1.IPSL-WRF381P.v1.day.pr.v20190212'
    ],
    'checks': ['RankCheck', 'OutlierRangeCheck', 'OtherCheck'],
    'proposed_fixes': [
        {
            'fix_id': 'RankFix',
            'dataset_id': 'c3s-cordex.output.EUR-11.IPSL.MOHC-HadGEM2-ES.rcp85.r1i1p1.IPSL-WRF381P.v1.day.pr.v20190212',
            'operands': {
                'rank': 2
            },
        },
        {
            'fix_id': 'OtherCheck',
            'dataset_id': 'c3s-cordex.output.EUR-11.IPSL.MOHC-HadGEM2-ES.rcp85.r1i1p1.IPSL-WRF381P.v1.day.tas.v20190212',
            'operands': {},
        }
    ],
    'analysis_metadata': {
        'location': 'ceda',
        'datetime': datetime.datetime.now(),
        'software_version': version
    }
}


