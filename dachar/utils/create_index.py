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

es = CEDAElasticsearchClient(
    headers={
        "x-api-key": ELASTIC_API_TOKEN
    }
)

#es.indices.delete(index="char-store-test", ignore=[400, 404])
print(es.indices.exists("roocs-char-test"))
es.indices.create("roocs-char-test")

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
    alias_exists = es.indices.exists_alias(name=f"{name}", index=f"{name}-{date}", params=None, headers=None)
    if not alias_exists:
        es.indices.put_alias(index=f"{name}-{date}", name=f"{name}", body=None, params=None, headers=None)


def populate_store(local_store, es_store):
    root = local_store.config.get('local.base_dir') #change if wanting to use a test store
    for path, subdirs, files in os.walk(root):
        for file in files:
            fpath = os.path.join(path, file)
            drs = '.'.join(fpath.split('/')[3:])
            doc = json.load(open(fpath))
            es_store.put(drs, doc)


if __name__ == '__main__':
    #create_index_and_alias(char_name)
    #populate_store(get_dc_store, get_dc_store('elasticsearch')
    pass
