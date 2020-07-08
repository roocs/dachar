from dachar.utils.json_store import _LocalBaseJsonStore, _ElasticSearchBaseJsonStore
from dachar.config import ELASTIC_API_TOKEN

class LocalAnalysisRecordsStore(_LocalBaseJsonStore):
    """
    Analysis Results Json Store: A JSON store to hold the results from the analysis of
    populations of ESGF Datasets.
    """

    store_name = "Analysis Results Store"
    config = {
        "store_type": "local",
        "local.base_dir": "/tmp/an-res-store",
        "local.dir_grouping_level": 4,
    }
    id_mappers = {"*": "__ALL__"}
    required_fields = [
        "sample_id",
        "dataset_ids",
        "checks",
        "proposed_fixes",
        "analysis_metadata",
    ]


class ElasticAnalysisRecordsStore(_ElasticSearchBaseJsonStore):

    store_name = "Analysis Results Store"
    config = {"store_type": "elasticsearch",
              "index": "roocs-analysis",
              "api_token": ELASTIC_API_TOKEN,
              "id_type": "sample_id"}
    id_mappers = {"*": "__ALL__"}
    required_fields = [
        "sample_id",
        "dataset_ids",
        "checks",
        "proposed_fixes",
        "analysis_metadata",
    ]
