from dachar.utils.json_store import _LocalBaseJsonStore, _ElasticSearchBaseJsonStore
from dachar import CONFIG


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
    config = {
        "store_type": "elasticsearch",
        "index": "roocs-char",
        "api_token": CONFIG['dachar:settings']['elastic_api_token'],
        "id_type": "dataset_id",
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
