from dachar.utils.json_store import _LocalBaseJsonStore, _ElasticSearchBaseJsonStore


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
    config = {"store_type": "elasticsearch", "index": "roocs-char"}
    id_mappers = {"*": "__ALL__"}
    required_fields = [
        "coordinates",
        "data",
        "global_attrs",
        "scan_metadata",
        "variable",
    ]  # ,
    #'coordinates.bounds']
