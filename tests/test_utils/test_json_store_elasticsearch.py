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


# Create a new dummy store to run tests on
class _TestStore(_ElasticSearchBaseJsonStore):

    store_name = "TestElasticsearchStore"
    config = {
        "store_type": "elasticsearch",
        "index": "roocs-char-test",
        "api_token": CONFIG["dachar:settings"]["elastic_api_token"],
        "id_type": "ds_id",
    }
    required_fields = ["d"]


store = None

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
    try:
        store = _TestStore()
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
def test_get():
    rec = store.get("1.2.3.4.5.6.b")
    assert rec["ds_id"] == "1.2.3.4.5.6.b"


@pytest.mark.skipif(
    CONFIG["dachar:settings"]["elastic_api_token"] == "",
    reason="cannot connect to elasticsearch",
)
def test_put_force_parameter():
    _id, content = recs[0]
    if not store.exists(_id):
        store.put(_id, content)

    with pytest.raises(FileExistsError) as exc:
        store.put(_id, content)
        assert (
            str(exc.value)
            == f'Record already exists: {_id}. Use "force=True" to overwrite.'
        )

    store.put(_id, content, force=True)


# def test_put_maps_asterisk():
#     _id = '1.1.*.1.*.*.1'
#     store.put(_id, {'data': 'test'})
#     fpath = store._id_to_path(_id)
#
#     bdir = store.config['local.base_dir']
#     assert(fpath == os.path.join(bdir, '1/1/__ALL__/1.__ALL__.__ALL__.1.json'))
#     assert(os.path.isfile(fpath))
#     store.delete(_id)


@pytest.mark.skipif(
    CONFIG["dachar:settings"]["elastic_api_token"] == "",
    reason="cannot connect to elasticsearch",
)
def test_delete():
    _id = recs[2][0]
    assert store.exists(_id)

    store.delete(_id)
    assert store.get(_id) is None


@pytest.mark.skipif(
    CONFIG["dachar:settings"]["elastic_api_token"] == "",
    reason="cannot connect to elasticsearch",
)
def test_validate_non_json():
    with pytest.raises(Exception) as exc:
        store._validate("rubbish")
        assert str(exc.value) == "Cannot serialise content to valid JSON."


@pytest.mark.skipif(
    CONFIG["dachar:settings"]["elastic_api_token"] == "",
    reason="cannot connect to elasticsearch",
)
def test_put_fail_validate():
    with pytest.raises(ValueError) as exc:
        store.put(*recs[1])
        assert str(exc.value).find('Required content "d" not found.') > -1


@pytest.mark.skipif(
    CONFIG["dachar:settings"]["elastic_api_token"] == "",
    reason="cannot connect to elasticsearch",
)
def test_get_all():
    time.sleep(5)  # sleep to ensure index has updated

    all = list(store.get_all())
    assert len(all) == 1


@pytest.mark.skipif(
    CONFIG["dachar:settings"]["elastic_api_token"] == "",
    reason="cannot connect to elasticsearch",
)
def test_get_all_ids():
    time.sleep(5)  # sleep to ensure index has updated

    all_ids = [_ for _ in store.get_all_ids()]
    assert len(all_ids) == 1


# @pytest.mark.xfail(reason="tox test fails")

# can not search for case insensitive wildcards for phrases but can for one word,
# cannot search exact=False for number fields (will change to exact=True if search term is a number)
# need to specify exact fields to search or search all (doesn't search nested
# field if only top level field is specified)


@pytest.mark.skipif(
    CONFIG["dachar:settings"]["elastic_api_token"] == "",
    reason="cannot connect to elasticsearch",
)
def test_search_by_term():
    store.put(recs[2][0], recs[2][1], force=True)
    store.put(recs[0][0], recs[0][1], force=True)
    time.sleep(5)

    # Search with custom fields + exact match
    resp = store.search("great match", exact=True, fields=["d"])
    assert resp[0]["d"] == recs[0][1]["d"]

    # Search with custom fields + partial match
    resp = store.search("at mat", exact=False, fields=["d"])
    assert resp[0]["d"] == recs[0][1]["d"]

    # Search with custom fields + partial match
    resp = store.search("at MAT", exact=False, fields=["d"])
    assert resp == []  # wildcard matching is case sensitive by default

    # Search with custom nested fields + exact match as integer
    resp = store.search(123, exact=True, fields=["z.d2.test1"])
    assert resp[0]["d"] == recs[2][1]["d"]
    assert resp[0]["z"] == recs[2][1]["z"]

    # Search with custom nested fields + inexact match as integer
    resp = store.search(123, exact=False, fields=["z.d2.test1"])
    assert resp[0]["d"] == recs[2][1]["d"]
    assert resp[0]["z"] == recs[2][1]["z"]

    # Search with exact match for string
    resp = store.search("123", exact=True, fields=["z.d2.test1"])
    assert resp[0]["d"] == recs[2][1]["d"]
    assert resp[0]["z"] == recs[2][1]["z"]

    # Search with partial match for string
    resp = store.search("123", exact=False, fields=["z", "ds_id"])
    assert resp == []  # elasticsearch doesn't search nested fields

    # Search with custom multiple fields and partial match
    with pytest.raises(exceptions.RequestError) as exc:
        store.search("e", exact=False, fields=["d", "z.d2.test1"])
        assert str(exc.value).find(
            "Can only use wildcard queries on keyword and text fields - "
            "not on [z.d2.test1] which is of type [long]"
        )

    # Search everything if no fields
    resp = store.search("e", exact=False, fields=None)
    assert resp[0]["d"] == recs[0][1]["d"]

    # Search with failed match
    resp = store.search("zzz", exact=False, fields=None)
    assert resp == []


@pytest.mark.skipif(
    CONFIG["dachar:settings"]["elastic_api_token"] == "",
    reason="cannot connect to elasticsearch",
)
def test_search_by_id():
    store.put(recs[2][0], recs[2][1], force=True)
    store.put(recs[0][0], recs[0][1], force=True)
    time.sleep(5)

    # Search for non-existent id
    resp = store.search("zzz", exact=False, match_ids=True)
    assert resp == []

    # Search by partial ID
    resp = store.search("5.6.b", exact=False, match_ids=True)
    assert resp[0]["d"] == recs[0][1]["d"]

    # Search for exact ID - WORKS
    resp = store.search(recs[0][0], exact=True, match_ids=True)
    assert resp[0]["d"] == recs[0][1]["d"]
    assert resp[0]["ds_id"] == recs[0][0]


def teardown_module():
    clear_store()
