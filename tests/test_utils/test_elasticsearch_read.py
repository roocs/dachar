# Tests for default JsonStore class
import os
import shutil
import time

import pytest
from ceda_elasticsearch_tools.elasticsearch import CEDAElasticsearchClient
from elasticsearch import Elasticsearch
from elasticsearch import exceptions

from dachar import CONFIG
from dachar.utils.json_store import _ElasticSearchBaseJsonStore


# Create dummy stores to run tests on - one with write access and one with read only
class _TestStore(_ElasticSearchBaseJsonStore):

    store_name = "TestElasticsearchStore"
    config = {
        "store_type": "elasticsearch",
        "index": "roocs-char-test",
        "api_token": CONFIG["dachar:settings"]["elastic_api_token"],
        "id_type": "ds_id",
    }


# Create dummy stores to run tests on - one with write access and one with read only
class _TestReadStore(_ElasticSearchBaseJsonStore):

    store_name = "TestElasticsearchStore"
    config = {
        "store_type": "elasticsearch",
        "index": "roocs-char-test",
        "id_type": "ds_id",
    }


store = None
read_store = None

recs = [
    ("1.2.3.4.5.6.b", {"d": "great match"}),
    ("1.2.3.4.5.6.a", {"x": "does not save"}),
    ("1.2.3.4.5.6.c", {"d": "cool", "z": {"d2": {"test1": 123, "test2": "hi"}}}),
]


def clear_store():
    for id in recs[0][0], recs[1][0], recs[2][0]:
        try:
            store.delete(id)
        except Exception:
            pass


def setup_module():
    # check elasticsearch connection - if fails - fail all tests
    global store
    global read_store
    try:
        store = _TestStore()
        read_store = _TestReadStore()
    except exceptions.AuthenticationException:
        pytest.exit("Connection to elasticsearch index failed")
    clear_store()


@pytest.mark.skipif(
    CONFIG["dachar:settings"]["elastic_api_token"] == "",
    reason="cannot connect to elasticsearch",
)
def test_verify_store():
    # Tests that the store gets created - via setup_module()
    pass


@pytest.mark.skipif(
    CONFIG["dachar:settings"]["elastic_api_token"] == "",
    reason="cannot connect to elasticsearch",
)
def test_put():
    store.put(recs[0][0], recs[0][1])
    store.put(recs[2][0], recs[2][1])
    assert store.exists(recs[0][0])
    assert store.exists(recs[2][0])


@pytest.mark.skipif(
    CONFIG["dachar:settings"]["elastic_api_token"] == "",
    reason="cannot connect to elasticsearch",
)
def test_read():
    rec = read_store.get("1.2.3.4.5.6.b")
    assert rec["ds_id"] == "1.2.3.4.5.6.b"
