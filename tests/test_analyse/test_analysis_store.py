import datetime
import os
import shutil

from dachar import __version__ as version
# Create a new dummy store to run tests on
from tests._stores_for_tests import _TestAnalysisStore


store = None


def _clear_store():
    dr = _TestAnalysisStore.config['local.base_dir']
    if os.path.isdir(dr):
        shutil.rmtree(dr)


def setup_module():
    _clear_store()
    global store
    store = _TestAnalysisStore()


eg_record = {
    'sample_id': 'c3s-cordex.output.EUR-11.IPSL.MOHC-HadGEM2-ES.rcp85.r1i1p1.IPSL-WRF381P.v1.day.*.v20190212',
    'dataset_ids': [
        'c3s-cordex.output.EUR-11.IPSL.MOHC-HadGEM2-ES.rcp85.r1i1p1.IPSL-WRF381P.v1.day.tas.v20190212',
        'c3s-cordex.output.EUR-11.IPSL.MOHC-HadGEM2-ES.rcp85.r1i1p1.IPSL-WRF381P.v1.day.pr.v20190212'
    ],
    'checks': ['RankCheck', 'OutlierRangeCheck', 'OtherCheck'],
    'proposed_fixes': [
        {
            'dataset_id': 'c3s-cordex.output.EUR-11.IPSL.MOHC-HadGEM2-ES.rcp85.r1i1p1.IPSL-WRF381P.v1.day.pr.v20190212',
            'fix': {'fix_id': 'RankFix',
                    'operands': {'rank': 2}}
        },
        {
            'dataset_id': 'c3s-cordex.output.EUR-11.IPSL.MOHC-HadGEM2-ES.rcp85.r1i1p1.IPSL-WRF381P.v1.day.tas.v20190212',
            'fix': {'fix_id': 'OtherCheck',
                    'operands': {}}
        }
    ],
    'analysis_metadata': {
        'location': 'ceda',
        'datetime': datetime.datetime.now(),
        'software_version': version
    }
}
