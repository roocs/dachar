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

from dachar.utils.get_stores import (
    get_fix_store,
    get_fix_prop_store,
    get_dc_store,
    get_ar_store,
)

from tests._stores_for_tests import _TestFixProposalStore, _TestFixStore, _TestAnalysisStore, _TestDatasetCharacterStore

es = CEDAElasticsearchClient(
    headers={
        "x-api-key": ELASTIC_API_TOKEN
    }
)

# es.indices.delete(index="roocs-char-test", ignore=[400, 404])
# print(es.indices.exists("roocs-char-test"))
# es.indices.create("roocs-char-test")

date = datetime.today().strftime('%Y-%m-%d')

# character store
char_name = 'roocs-char'
# analysis store
a_name = 'roocs-analysis'
# fix store
fix_name = 'roocs-fix'
# fix proposal store
fix_prop_name = 'roocs-fix-prop'


def create_index_and_alias(name):
    exists = es.indices.exists(f"{name}-{date}")
    if not exists:
        es.indices.create(f"{name}-{date}") # do I need to include a mapping - should be put in here
    alias_exists = es.indices.exists_alias(name=f"{name}", index=f"{name}-{date}")
    if not alias_exists:
        es.indices.put_alias(index=f"{name}-{date}", name=f"{name}")


def populate_store(local_store, index, id_type):
    root = local_store.config.get('local.base_dir') #change if wanting to use a test store
    for path, subdirs, files in os.walk(root):
        for file in files:
            fpath = os.path.join(path, file)
            drs = '.'.join(fpath.split('/')[3:])
            m = hashlib.md5()
            m.update(drs.encode("utf-8"))
            id = m.hexdigest()
            doc = json.load(open(fpath))
            es.index(index=index, id=id, body=doc)
            es.update(index=index,
                           id=id, body={"doc": {id_type: drs}})


def main():
    # for store in [char_name, a_name, fix_name, fix_prop_name]:
    #     create_index_and_alias(store)

    populate_store(_TestAnalysisStore(), 'roocs-analysis-2020-07-08', 'sample_id')


if __name__ == '__main__':
    main()
