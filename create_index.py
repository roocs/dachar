import sys
import os
import pathlib
import hashlib
import json
from elasticsearch import Elasticsearch
from ceda_elasticsearch_tools.elasticsearch import CEDAElasticsearchClient

es = CEDAElasticsearchClient(headers={'x-api-key': 'cdad90eaf6f889732fd691e38df2f6456e9f73029b3a49f0a871d5f64a553c44'})


#print(es.indices.exists("char-store-test"))
#es.indices.create("char-store-test")

root = "/tmp/test-ds-char-store"

for path, subdirs, files in os.walk(root):
    for file in files:
        fpath = os.path.join(path, file)
        drs = '.'.join(fpath.split('/')[3:])
        print(drs)
        # m = hashlib.md5()
        # m.update(drs.encode('utf-8'))
        # id = m.hexdigest()
        # print(id)
        # doc = json.load(open(fpath))
        # es.index("char-store-test", doc, id=id)

