import os
import shutil
import subprocess
from unittest.mock import Mock

import mock
import pytest

from dachar.fixes import generate_proposals
from dachar.utils.common import now_string
from tests._stores_for_tests import _TestFixProposalStore

prop_store = None
cwd = os.getcwd()


def clear_store():
    fp_dr = _TestFixProposalStore.config["local.base_dir"]
    if os.path.isdir(fp_dr):
        shutil.rmtree(fp_dr)


def setup_module():
    clear_store()
    global prop_store
    prop_store = _TestFixProposalStore()


def test_generate_proposal_json():
    file = [f"{cwd}/tests/test_fixes/decadal_fixes/decadal.json"]

    generate_proposals.get_fix_prop_store = Mock(return_value=prop_store)

    generate_proposals.generate_fix_proposals(file)
    record = prop_store.get_proposed_fix_by_id(
        "c3s-cmip6.DCPP.MOHC.HadGEM3-GC31-MM.dcppA-hindcast.s2004-r3i1p1f2.Amon.pr.gn.v20200417"
    )
    assert record[0]["this_fix"]["fix"]["fix_id"] == "VarAttrFix"
    clear_store()


def test_generate_proposal_json_2_fixes():

    file = [
        {
            "dataset_id": "c3s-cmip6.DCPP.MOHC.HadGEM3-GC31-MM.dcppA-hindcast.s2004-r3i1p1f2.Amon.pr.gn.v20200417",
            "fixes": [
                {
                    "fix_id": "VarAttrFix",
                    "operands": {
                        "var_id": "time",
                        "attrs": {"long_name": "valid_time"},
                    },
                    "source": {
                        "name": "ceda",
                        "version": "",
                        "comments": "",
                        "url": "https://github.com/cp4cds/c3s34g_master/tree/master/Decadal",
                    },
                },
                {
                    "fix_id": "GlobalAttrFix",
                    "operands": {
                        "attrs": {
                            "forcing_description": "Free text describing the forcings",
                            "physics_description": "Free text describing the physics method",
                            "initialization_description": "Free text describing the initialization method",
                            "startdate": "s200411",
                            "sub_experiment_id": "s200411",
                        }
                    },
                    "source": {
                        "name": "ceda",
                        "version": "",
                        "comments": "",
                        "url": "https://github.com/cp4cds/c3s34g_master/tree/master/Decadal",
                    },
                },
            ],
        }
    ]

    generate_proposals.get_fix_prop_store = Mock(return_value=prop_store)

    generate_proposals.generate_fix_proposals(file)
    record = prop_store.get_proposed_fix_by_id(
        "c3s-cmip6.DCPP.MOHC.HadGEM3-GC31-MM.dcppA-hindcast.s2004-r3i1p1f2.Amon.pr.gn.v20200417"
    )
    assert record[0]["this_fix"]["fix"]["fix_id"] == "VarAttrFix"
    assert record[1]["this_fix"]["fix"]["fix_id"] == "GlobalAttrFix"

    clear_store()


def test_generate_proposal_template():
    ds_list = f"{cwd}/tests/test_fixes/decadal_fixes/decadal_fix_list.txt"
    template = f"{cwd}/tests/test_fixes/decadal_fixes/decadal_template.json"

    generate_proposals.get_fix_prop_store = Mock(return_value=prop_store)

    generate_proposals.generate_proposal_from_template(template, ds_list)
    record = prop_store.get_proposed_fix_by_id(
        "c3s-cmip6.DCPP.MOHC.HadGEM3-GC31-MM.dcppA-hindcast.s2004-r3i1p1f2.Amon.pr.gn.v20200417"
    )
    assert record[0]["this_fix"]["fix"]["fix_id"] == "VarAttrFix"


def test_generate_proposal_when_one_already_exists():
    file = [
        {
            "dataset_id": "c3s-cmip6.DCPP.MOHC.HadGEM3-GC31-MM.dcppA-hindcast.s2004-r3i1p1f2.Amon.pr.gn.v20200417",
            "fixes": [
                {
                    "fix_id": "CheckAddGlobalAttrFix",
                    "operands": {"attrs": {"test": "test"}},
                    "source": {
                        "name": "ceda",
                        "version": "",
                        "comments": "",
                        "url": "https://github.com/cp4cds/c3s34g_master/tree/master/Decadal",
                    },
                }
            ],
        }
    ]

    generate_proposals.get_fix_prop_store = Mock(return_value=prop_store)

    generate_proposals.generate_fix_proposals(file)
    record = prop_store.get_proposed_fix_by_id(
        "c3s-cmip6.DCPP.MOHC.HadGEM3-GC31-MM.dcppA-hindcast.s2004-r3i1p1f2.Amon.pr.gn.v20200417"
    )
    assert record[0]["this_fix"]["fix"]["fix_id"] == "VarAttrFix"
    assert record[-1]["this_fix"]["fix"]["fix_id"] == "CheckAddGlobalAttrFix"


def test_unexpected_operands():
    file = [
        {
            "dataset_id": "c3s-cmip6.DCPP.MOHC.HadGEM3-GC31-MM.dcppA-hindcast.s2004-r3i1p1f2.Amon.pr.gn.v20200417",
            "fixes": [
                {
                    "fix_id": "VarAttrFix",
                    "operands": {"var_id": "pr", "attrs": {}, "test": "not_real"},
                    "source": {
                        "name": "ceda",
                        "version": "",
                        "comments": "",
                        "url": "https://github.com/cp4cds/c3s34g_master/tree/master/Decadal",
                    },
                }
            ],
        }
    ]

    generate_proposals.get_fix_prop_store = Mock(return_value=prop_store)

    with pytest.raises(KeyError) as exc:
        generate_proposals.generate_fix_proposals(file)
    assert exc.value.args[0] == "Invalid keyword arguments received: {'test'}"


def test_missing_operands():
    file = [
        {
            "dataset_id": "c3s-cmip6.DCPP.MOHC.HadGEM3-GC31-MM.dcppA-hindcast.s2004-r3i1p1f2.Amon.pr.gn.v20200417",
            "fixes": [
                {
                    "fix_id": "VarAttrFix",
                    "operands": {"var_id": "pr", "test": "not_real"},
                    "source": {
                        "name": "ceda",
                        "version": "",
                        "comments": "",
                        "url": "https://github.com/cp4cds/c3s34g_master/tree/master/Decadal",
                    },
                }
            ],
        }
    ]

    generate_proposals.get_fix_prop_store = Mock(return_value=prop_store)

    with pytest.raises(KeyError) as exc:
        generate_proposals.generate_fix_proposals(file)
    assert exc.value.args[0] == "Required keyword argument(s) not provided: {'attrs'}"


def test_invalid_fields():
    file = [
        {
            "dataset_id": "c3s-cmip6.DCPP.MOHC.HadGEM3-GC31-MM.dcppA-hindcast.s2004-r3i1p1f2.Amon.pr.gn.v20200417",
            "fixes": [
                {
                    "fox_id": "VarAttrFix",
                    "operands": {"test": "not_real"},
                    "source": {
                        "name": "ceda",
                        "version": "",
                        "comments": "",
                        "url": "https://github.com/cp4cds/c3s34g_master/tree/master/Decadal",
                    },
                }
            ],
        }
    ]

    generate_proposals.get_fix_prop_store = Mock(return_value=prop_store)

    with pytest.raises(KeyError) as exc:
        generate_proposals.generate_fix_proposals(file)
    assert exc.value.args[0] == "Required fields not provided: {'fix_id'}"


def test_missing_fields():
    file = [
        {
            "dataset_id": "cmip5.output1.MOHC.HadGEM2-CC.historical.yr.ocnBgchem.Oyr.r1i1p1.latest.o2",
            "fixes": [
                {
                    "fix_id": "MainVarAttrFix",
                    "source": {
                        "name": "ceda",
                        "version": "",
                        "comments": "",
                        "url": "https://github.com/cp4cds/c3s34g_master/tree/master/Decadal",
                    },
                }
            ],
        }
    ]

    generate_proposals.get_fix_prop_store = Mock(return_value=prop_store)

    with pytest.raises(KeyError) as exc:
        generate_proposals.generate_fix_proposals(file)
    assert exc.value.args[0] == "Required fields not provided: {'operands'}"


def teardown_module():
    # pass
    clear_store()
