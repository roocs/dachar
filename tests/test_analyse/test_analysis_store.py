import datetime
import os
import shutil

from dachar import __version__ as version

# Create a new dummy store to run tests on
from tests._stores_for_tests import _TestAnalysisStore
from dachar.analyse.sample_analyser import AnalysisRecord


store = None
sample_id = "cmip5.output1.*.*.rcp45.mon.ocean.Omon.r1i1p1.latest.zostoga"


def _clear_store():
    dr = _TestAnalysisStore.config["local.base_dir"]
    if os.path.isdir(dr):
        shutil.rmtree(dr)


def setup_module():
    _clear_store()
    global store
    store = _TestAnalysisStore()

    
def test_put():
    ds_ids = ["cmip5.output1.MOHC.HadGEM2-ES.rcp45.mon.ocean.Omon.r1i1p1.latest.zostoga", 
              "cmip5.output1.INM.inmcm4.rcp45.mon.ocean.Omon.r1i1p1.latest.zostoga"]
    a_record = AnalysisRecord(sample_id, ds_ids, "ceda", ["coord_checks.RankCheck", "coord_checks.MissingCoordCheck"])
    store.put(sample_id, a_record.content, force=True)
    assert store.exists(sample_id)


def test_get():
    record = store.get(sample_id)
    assert record['checks'] == ["coord_checks.RankCheck", "coord_checks.MissingCoordCheck"]
    assert record['analysis_metadata'] == {'datetime': (datetime.datetime.now()).strftime("%d/%m/%Y, %H:%M"),
                                           'location': 'ceda', 
                                           'software_version': '0.1.0'}
    assert record['dataset_ids'] == ['cmip5.output1.MOHC.HadGEM2-ES.rcp45.mon.ocean.Omon.r1i1p1.latest.zostoga',
                                     'cmip5.output1.INM.inmcm4.rcp45.mon.ocean.Omon.r1i1p1.latest.zostoga']
    assert record['proposed_fixes'] == []
    assert record['sample_id'] == 'cmip5.output1.*.*.rcp45.mon.ocean.Omon.r1i1p1.latest.zostoga'


def test_delete():
    store.delete(sample_id)
    assert not store.exists(sample_id)


def teardown_module():
    _clear_store()


eg_record = {
    "sample_id": "c3s-cordex.output.EUR-11.IPSL.MOHC-HadGEM2-ES.rcp85.r1i1p1.IPSL-WRF381P.v1.day.*.v20190212",
    "dataset_ids": [
        "c3s-cordex.output.EUR-11.IPSL.MOHC-HadGEM2-ES.rcp85.r1i1p1.IPSL-WRF381P.v1.day.tas.v20190212",
        "c3s-cordex.output.EUR-11.IPSL.MOHC-HadGEM2-ES.rcp85.r1i1p1.IPSL-WRF381P.v1.day.pr.v20190212",
    ],
    "checks": ["RankCheck", "OutlierRangeCheck", "OtherCheck"],
    "proposed_fixes": [
        {
            "dataset_id": "c3s-cordex.output.EUR-11.IPSL.MOHC-HadGEM2-ES.rcp85.r1i1p1.IPSL-WRF381P.v1.day.pr.v20190212",
            "fix": {"fix_id": "RankFix", "operands": {"rank": 2}},
        },
        {
            "dataset_id": "c3s-cordex.output.EUR-11.IPSL.MOHC-HadGEM2-ES.rcp85.r1i1p1.IPSL-WRF381P.v1.day.tas.v20190212",
            "fix": {"fix_id": "OtherCheck", "operands": {}},
        },
    ],
    "analysis_metadata": {
        "location": "ceda",
        "datetime": datetime.datetime.now(),
        "software_version": version,
    },
}