from dachar.utils.json_store import _LocalBaseJsonStore, _ElasticSearchBaseJsonStore
from dachar.config import ELASTIC_API_TOKEN

class LocalDatasetCharacterStore(_LocalBaseJsonStore):

    store_name = "Dataset Character Store"
    config = {
        "store_type": "local",
        "local.base_dir": "/tmp/ds-char-store",
        "local.dir_grouping_level": 4,
    }
    id_mappers = {"*": "__ALL__"}
    required_fields = [
        "coordinates",
        "data",
        "global_attrs",
        "scan_metadata",
        "variable",
    ]  # ,
    #'coordinates.bounds']


class ElasticDatasetCharacterStore(_ElasticSearchBaseJsonStore):

    store_name = "Dataset Character Store"
    config = {"store_type": "elasticsearch",
              "index": "roocs-char",
              "api_token": ELASTIC_API_TOKEN,
              "id_type": "ds_id"}
    id_mappers = {"*": "__ALL__"}
    required_fields = [
        "coordinates",
        "data",
        "global_attrs",
        "scan_metadata",
        "variable",
    ]  # ,
    #'coordinates.bounds']
