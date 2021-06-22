"""
This script can produce an index with today's date and update the alias to point to it.
There is also a function to populate the elasticsearch store with the contents of the local store.

When updating the index:
- new index must be created with new date - clone_index_and_update_alias function creates this, fills with all documents from old index and updates the alias to point to it if update_alias is True
- it can then be populated either with all documents in local store (populate_store) or one document at a time (add_document_to_index)
"""
import hashlib
import json
import os
import pathlib
import sys
from datetime import datetime

from ceda_elasticsearch_tools.elasticsearch import CEDAElasticsearchClient
from elasticsearch import Elasticsearch

from dachar import CONFIG
from dachar.utils.get_stores import get_ar_store
from dachar.utils.get_stores import get_dc_store
from dachar.utils.get_stores import get_fix_prop_store
from dachar.utils.get_stores import get_fix_store

# from tests._stores_for_tests import (
#     _TestFixProposalStore,
#     _TestFixStore,
#     _TestAnalysisStore,
#     _TestDatasetCharacterStore,
# )

if not CONFIG["dachar:settings"]["elastic_api_token"]:
    raise Exception(
        "Elastic api token must be set in the config to be able to create, delete or write to indices."
    )
else:
    es = CEDAElasticsearchClient(
        headers={"x-api-key": CONFIG["dachar:settings"]["elastic_api_token"]}
    )


def delete_index(index_name):
    """
    Delete an index
    """
    es.indices.delete(index=index_name, ignore=[400, 404])
    print(f"Deleted index {index_name}")


def create_index_and_alias(index_name, update_alias=False):
    """
    create an empty index and if update_alias is True then update the alias to point to it (default is False)
    """
    date = datetime.today().strftime("%Y-%m-%d")

    exists = es.indices.exists(f"{index_name}-{date}")
    if not exists:
        es.indices.create(f"{index_name}-{date}")

    if update_alias:
        update_alias(f"{index_name}-{date}")

    print(f"Created index {index_name}-{date} with alias {index_name}")


def update_alias(index_name):
    index_alias = ("-").join(index_name.split("-")[:-3])
    alias_exists = es.indices.exists_alias(name=f"{index_alias}", index=f"{index_name}")
    if not alias_exists:
        es.indices.update_aliases(
            body={
                "actions": [
                    {"remove": {"alias": f"{index_alias}", "index": "*"}},
                    {"add": {"alias": f"{index_alias}", "index": f"{index_name}",}},
                ]
            }
        )


def clone_index_and_update_alias(index_name, index_to_clone, update_alias=False):
    """
    clone an index and if update_alias is True then update the alias to point to it (default is False)
    """
    date = datetime.today().strftime("%Y-%m-%d")

    exists = es.indices.exists(f"{index_name}-{date}")
    if not exists:
        es.indices.create(f"{index_name}-{date}")
    es.reindex(
        body={
            "source": {"index": f"{index_to_clone}"},
            "dest": {"index": f"{index_name}-{date}"},
        }
    )
    if update_alias:
        update_alias(f"{index_name}-{date}")

    print(
        f"Cloned index {index_to_clone} to index {index_name}-{date} with alias {index_name}"
    )


def populate_store(local_store, index, id_type):
    """
    Populates elasticsearch index from local store
    :param local_store: local store object to populate from
    :param index: Name of elasticsearch index to populate
    :param id_type: what the id is called in the provided index i.e. either dataset_id (for fix, character and fix proposal store) or sample_id (for the analysis store)
    """

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

            m = hashlib.md5()
            m.update(drs.encode("utf-8"))
            doc_id = m.hexdigest()
            doc = json.load(open(fpath))

            es.index(index=index, id=doc_id, body=doc)
            if id_type is not None:
                es.update(index=index, id=doc_id, body={"doc": {id_type: drs}})

            print(
                f"Added document for {drs} from loacal store {local_store} in index {index}"
            )


def add_document_to_index(fpath, drs, index, id_type):
    """
    Add document to elasticsearch index. Uses given file path to json file and ds_id (drs).
    """

    mapper = {"__ALL__": "*"}
    for find_s, replace_s in mapper.items():
        drs = drs.replace(find_s, replace_s)

    m = hashlib.md5()
    m.update(drs.encode("utf-8"))
    doc_id = m.hexdigest()
    doc = json.load(open(fpath))

    es.index(index=index, id=doc_id, body=doc)
    if id_type is not None:
        es.update(index=index, id=doc_id, body={"doc": {id_type: drs}})

    print(f"Added document for {drs} from path {fpath} in index {index}")
