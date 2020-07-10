import os
import shutil
import subprocess
import mock
import pytest

from tests._stores_for_tests import _TestFixProposalStore, _TestFixStore
from dachar.fixes import fix_processor
from dachar.utils.common import now_string


from unittest.mock import Mock

ds_ids = [
    "ds.1.1.1.1.1.1",
    "ds.2.1.1.1.1.1",
    "ds.3.1.1.1.1.1",
    "ds.4.1.1.1.1.1",
    "ds.5.1.1.1.1.1",
]

fixes = [
    {
        "fix_id": "Fix1",
        "title": "Apply Fix 1",
        "description": "Applies fix 1",
        "category": "test_fixes",
        "reference_implementation": "daops.test.test_fix1",
        "operands": {"arg1": "1"},
    },
    {
        "fix_id": "Fix2",
        "title": "Apply Fix 2",
        "description": "Applies fix 2",
        "category": "test_fixes",
        "reference_implementation": "daops.test.test_fix2",
        "operands": {"arg2": "2"},
    },
    {
        "fix_id": "Fix3",
        "title": "Apply Fix 3",
        "description": "Applies fix 3",
        "category": "test_fixes",
        "reference_implementation": "daops.test.test_fix3",
        "operands": {"arg3": "3"},
    },
    {
        "fix_id": "Fix by id",
        "title": "Apply Fix by id",
        "description": "Applies fix ",
        "category": "test_fixes",
        "reference_implementation": "daops.test.test_fix_by_id",
        "operands": {"arg4": "4"},
    },
    {
        "fix_id": "Fix 5 by id",
        "title": "Apply Fix 5 by id",
        "description": "Applies fix 5",
        "category": "test_fixes",
        "reference_implementation": "daops.test.test_fix5",
        "operands": {"arg4": "5"},
    },
]

prop_store = None
f_store = None


def clear_stores():
    fp_dr = _TestFixProposalStore.config["local.base_dir"]
    f_dr = _TestFixStore.config["local.base_dir"]
    for dr in [fp_dr, f_dr]:
        if os.path.isdir(dr):
            shutil.rmtree(dr)


def setup_module():
    clear_stores()
    global prop_store
    global f_store
    prop_store = _TestFixProposalStore()
    f_store = _TestFixStore()


def generate_fix_proposal(id, fix):
    prop_store.propose(id, fix)


def generate_published_fix(id, fix):
    prop_store.publish(id, fix)


def id_to_fix_path(ds_id):
    parts = ds_id.split(".")
    grouped_id = "/".join(parts[:-4]) + "/" + ".".join(parts[-4:])
    fpath = os.path.join("/tmp/test-fix-store", grouped_id + ".json")
    return fpath


# tests 2 proposed fixes returned
def test_get_2_proposed_fixes():
    generate_fix_proposal(ds_ids[0], fixes[0])
    generate_fix_proposal(ds_ids[1], fixes[1])

    fix_processor.get_fix_prop_store = Mock(return_value=prop_store)

    proposed_fixes = fix_processor.get_proposed_fixes()

    assert len(proposed_fixes) == 2

    assert (proposed_fixes[0]) == {
        "dataset_id": "ds.1.1.1.1.1.1",
        "fixes": [
            {
                "fix": {
                    "category": "test_fixes",
                    "description": "Applies fix 1",
                    "fix_id": "Fix1",
                    "operands": {"arg1": "1"},
                    "reference_implementation": "daops.test.test_fix1",
                    "title": "Apply Fix 1",
                },
                "history": [],
                "reason": "",
                "status": "proposed",
                "timestamp": now_string(),
            }
        ],
    }

    assert proposed_fixes[1] == {
        "dataset_id": "ds.2.1.1.1.1.1",
        "fixes": [
            {
                "fix": {
                    "category": "test_fixes",
                    "description": "Applies fix 2",
                    "fix_id": "Fix2",
                    "operands": {"arg2": "2"},
                    "reference_implementation": "daops.test.test_fix2",
                    "title": "Apply Fix 2",
                },
                "history": [],
                "reason": "",
                "status": "proposed",
                "timestamp": now_string(),
            }
        ],
    }


# tests only one proposed fix returned as other fix is now published
def test_get_1_proposed_fixes():

    generate_published_fix(ds_ids[1], fixes[1])

    fix_processor.get_fix_prop_store = Mock(return_value=prop_store)

    proposed_fixes = fix_processor.get_proposed_fixes()

    assert prop_store.exists(ds_ids[0])
    assert prop_store.exists(ds_ids[1])
    assert len(proposed_fixes) == 1
    assert proposed_fixes[0] == {
        "dataset_id": "ds.1.1.1.1.1.1",
        "fixes": [
            {
                "fix": {
                    "category": "test_fixes",
                    "description": "Applies fix 1",
                    "fix_id": "Fix1",
                    "operands": {"arg1": "1"},
                    "reference_implementation": "daops.test.test_fix1",
                    "title": "Apply Fix 1",
                },
                "history": [],
                "reason": "",
                "status": "proposed",
                "timestamp": now_string(),
            }
        ],
    }


def test_process_proposed_fixes(monkeypatch):
    fix_processor.get_fix_prop_store = Mock(return_value=prop_store)
    fix_processor.get_fix_store = Mock(return_value=f_store)
    generate_fix_proposal(ds_ids[2], fixes[2])
    monkeypatch.setattr("builtins.input", lambda _: "publish")

    fix_processor.process_all_fixes("process")
    assert os.path.exists(id_to_fix_path(ds_ids[2]))


def test_process_proposed_fixes_with_id(monkeypatch):
    fix_processor.get_fix_prop_store = Mock(return_value=prop_store)
    fix_processor.get_fix_store = Mock(return_value=f_store)
    generate_fix_proposal(ds_ids[3], fixes[3])
    monkeypatch.setattr("builtins.input", lambda _: "publish")

    fix_processor.process_all_fixes("process", [ds_ids[3]])
    assert os.path.exists(id_to_fix_path(ds_ids[3]))


def test_withdraw_fix(monkeypatch):
    fix_processor.get_fix_prop_store = Mock(return_value=prop_store)
    fix_processor.get_fix_store = Mock(return_value=f_store)
    generate_fix_proposal(ds_ids[4], fixes[4])
    generate_published_fix(ds_ids[4], fixes[4])
    f_store.publish_fix(ds_ids[4], fixes[4])

    responses = iter(["y", "Fix 5 by id", "test"])
    monkeypatch.setattr("builtins.input", lambda _: next(responses))
    
    fix_processor.process_all_fixes("withdraw", [ds_ids[4]])

    assert os.path.exists(id_to_fix_path(ds_ids[4])) is False


def test_withdraw_with_2_fixes(monkeypatch):
    fix_processor.get_fix_prop_store = Mock(return_value=prop_store)
    fix_processor.get_fix_store = Mock(return_value=f_store)
    generate_fix_proposal(ds_ids[4], fixes[4])
    generate_published_fix(ds_ids[4], fixes[4])
    f_store.publish_fix(ds_ids[4], fixes[4])
    generate_fix_proposal(ds_ids[4], fixes[3])
    generate_published_fix(ds_ids[4], fixes[3])
    f_store.publish_fix(ds_ids[4], fixes[3])

    monkeypatch.setattr("builtins.input", lambda _: "n")

    fix_processor.process_all_fixes("withdraw", [ds_ids[4]])

    assert os.path.exists(id_to_fix_path(ds_ids[4]))


def test_withdraw_fix_not_found():
    fix_processor.get_fix_prop_store = Mock(return_value=prop_store)
    fix_processor.get_fix_store = Mock(return_value=f_store)
    with pytest.raises(Exception) as exc:
        fix_processor.process_all_fixes("withdraw", [ds_ids[1]])
        assert exc.value == "A fix could not be found."


def teardown_module():
    # pass
    clear_stores()
