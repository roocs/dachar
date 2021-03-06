"""
Currently this script produces a index with today's date and creates an alias for it.
There is a function to populate the elasticsearch store with the contents of the local store
"""

import sys
import os
import pathlib
import hashlib
import json
from datetime import datetime
from elasticsearch import Elasticsearch
from ceda_elasticsearch_tools.elasticsearch import CEDAElasticsearchClient
from dachar.config import ELASTIC_API_TOKEN
from dachar import CONFIG

from dachar.utils.get_stores import (
    get_fix_store,
    get_fix_prop_store,
    get_dc_store,
    get_ar_store,
)

from tests._stores_for_tests import (
    _TestFixProposalStore,
    _TestFixStore,
    _TestAnalysisStore,
    _TestDatasetCharacterStore,
)

es = CEDAElasticsearchClient(headers={"x-api-key": ELASTIC_API_TOKEN})

# es.indices.delete(index="roocs-char-test", ignore=[400, 404])
# print(es.indices.exists("roocs-char-test"))
# es.indices.create("roocs-char-test")

date = datetime.today().strftime("%Y-%m-%d")

# character store
char_name = CONFIG['elasticsearch']["character_store"]
# analysis store
a_name = CONFIG['elasticsearch']["analysis_store"]
# fix store
fix_name = CONFIG['elasticsearch']["fix_store"]
# fix proposal store
fix_prop_name = CONFIG['elasticsearch']["fix_proposal_store"]


def create_index_and_alias(name):
    exists = es.indices.exists(f"{name}-{date}")
    if not exists:
        es.indices.create(
            f"{name}-{date}"
        )  # do I need to include a mapping - should be put in here
    alias_exists = es.indices.exists_alias(name=f"{name}", index=f"{name}-{date}")
    if not alias_exists:
        es.indices.put_alias(index=f"{name}-{date}", name=f"{name}")


def populate_store(local_store, index, id_type):
    root = local_store.config.get(
        "local.base_dir"
    )  # change if wanting to use a test store
    for path, subdirs, files in os.walk(root):
        for file in files:
            fpath = os.path.join(path, file)
            drs = ".".join(fpath.split("/")[3:])
            drs = ".".join(drs.split(".")[:-1])

            mapper = {"__ALL__": "*"}
            for find_s, replace_s in mapper.items():
                drs = drs.replace(find_s, replace_s)

            print(drs)
            m = hashlib.md5()
            m.update(drs.encode("utf-8"))
            id = m.hexdigest()
            doc = json.load(open(fpath))
            # es.delete(index=index, id=id)

            es.index(index=index, id=id, body=doc)
            if id_type is not None:
                es.update(index=index, id=id, body={"doc": {id_type: drs}})


def main():
    # for store in [char_name, a_name, fix_name, fix_prop_name]:
    #     create_index_and_alias(store)

    populate_store(_TestDatasetCharacterStore(), "roocs-char-2020-07-08", "dataset_id")


if __name__ == "__main__":
    main()
