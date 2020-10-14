import os
import shutil
import subprocess
import mock
import pytest

from tests._stores_for_tests import _TestFixProposalStore
from dachar.fixes import generate_proposals
from dachar.utils.common import now_string
from unittest.mock import Mock

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
    file = [f"{cwd}/tests/test_fixes/esmval_test_fixes/o2.json"]

    generate_proposals.get_fix_prop_store = Mock(return_value=prop_store)

    generate_proposals.generate_fix_proposals(file)
    record = prop_store.get_proposed_fix_by_id(
        "cmip5.output1.MOHC.HadGEM2-CC.historical.yr.ocnBgchem.Oyr.r1i1p1.latest.o2")
    assert record[0]["this_fix"]["fix"]["fix_id"] == "MainVarAttrFix"


def test_generate_proposal_json_2_fixes():

    file = [{
        "dataset_id": "cmip5.output1.MOHC.HadGEM2-CC.historical.yr.ocnBgchem.Oyr.r1i1p1.latest.o2",
        "fixes": [{
            "fix_id": "MainVarAttrFix",
            "operands": {
                "attrs": [
                    "long_name,Dissolved Oxygen Concentration",
                    "standard_name,mole_concentration_of_dissolved_molecular_oxygen_in_sea_water"
                ]},
            "source": {
                    "name": "",
                    "version": "",
                    "comments": "testing 2 fixes proposed externally",
                    "url": ""}},
            {
                "fix_id": "SqueezeDimensionsFix",
                "operands": {
                    "dims": [
                        "test"
                    ]},
                "source": {
                    "name": "",
                    "version": "",
                    "comments": "testing 2 fixes proposed externally",
                    "url": ""}
            }]
    }]

    generate_proposals.get_fix_prop_store = Mock(return_value=prop_store)

    generate_proposals.generate_fix_proposals(file)
    record = prop_store.get_proposed_fix_by_id(
        "cmip5.output1.MOHC.HadGEM2-CC.historical.yr.ocnBgchem.Oyr.r1i1p1.latest.o2")
    assert record[0]["this_fix"]["fix"]["fix_id"] == "MainVarAttrFix"
    assert record[1]["this_fix"]["fix"]["fix_id"] == "SqueezeDimensionsFix"


def test_generate_proposal_template():
    ds_list = f"{cwd}/tests/test_fixes/esmval_test_fixes/o2_fix_ds_list.txt"
    template = f"{cwd}/tests/test_fixes/esmval_test_fixes/o2_template.json"

    generate_proposals.get_fix_prop_store = Mock(return_value=prop_store)

    generate_proposals.generate_proposal_from_template(template, ds_list)
    record = prop_store.get_proposed_fix_by_id(
        "cmip5.output1.MOHC.HadGEM2-CC.rcp85.mon.ocnBgchem.Omon.r1i1p1.v20120531.o2")
    assert record[0]["this_fix"]["fix"]["fix_id"] == "MainVarAttrFix"


def test_generate_proposal_when_one_already_exists():
    file = [{
        "dataset_id": "cmip5.output1.MOHC.HadGEM2-CC.rcp85.mon.ocnBgchem.Omon.r1i1p1.v20120531.o2",
        "fixes": [
            {
                "fix_id": "SqueezeDimensionsFix",
                "operands": {
                    "dims": [
                        "test"
                    ]},
                "source": {
                    "name": "",
                    "version": "",
                    "comments": "testing 2 fixes proposed externally",
                    "url": ""}}]
    }]

    generate_proposals.get_fix_prop_store = Mock(return_value=prop_store)

    generate_proposals.generate_fix_proposals(file)
    record = prop_store.get_proposed_fix_by_id(
        "cmip5.output1.MOHC.HadGEM2-CC.rcp85.mon.ocnBgchem.Omon.r1i1p1.v20120531.o2")
    assert record[0]["this_fix"]["fix"]["fix_id"] == "MainVarAttrFix"
    assert record[1]["this_fix"]["fix"]["fix_id"] == "SqueezeDimensionsFix"


def test_unexpected_operands():
    file = [{
        "dataset_id": "cmip5.output1.MOHC.HadGEM2-CC.historical.yr.ocnBgchem.Oyr.r1i1p1.latest.o2",
        "fixes": [{
            "fix_id": "MainVarAttrFix",
            "operands": {
                "test": [
                    "not_real"
                ]},
            "source": {
                "name": "esmvaltool",
                "version": "2.0.0",
                "comments": "",
                "url": "https://github.com/ESMValGroup/ESMValCore/blob/master/esmvalcore/cmor/_fixes/cmip5/hadgem2_cc.py#L34-L55"}
        }]
    }]

    generate_proposals.get_fix_prop_store = Mock(return_value=prop_store)

    with pytest.raises(KeyError) as exc:
        generate_proposals.generate_fix_proposals(file)
    assert exc.value.args[0] == "Required keyword argument(s) not provided: {'attrs'}"


def test_invalid_fields():
    file = [{
        "dataset_id": "cmip5.output1.MOHC.HadGEM2-CC.historical.yr.ocnBgchem.Oyr.r1i1p1.latest.o2",
        "fixes": [{
            "fox_id": "MainVarAttrFix",
            "operands": {
                "attrs": [
                    "not_real"
                ]},
            "source": {
                "name": "esmvaltool",
                "version": "2.0.0",
                "comments": "",
                "url": "https://github.com/ESMValGroup/ESMValCore/blob/master/esmvalcore/cmor/_fixes/cmip5/hadgem2_cc.py#L34-L55"}
        }]
    }]

    generate_proposals.get_fix_prop_store = Mock(return_value=prop_store)

    with pytest.raises(KeyError) as exc:
        generate_proposals.generate_fix_proposals(file)
    assert exc.value.args[0] == "Required fields not provided: {'fix_id'}"


def test_missing_fields():
    file = [{
        "dataset_id": "cmip5.output1.MOHC.HadGEM2-CC.historical.yr.ocnBgchem.Oyr.r1i1p1.latest.o2",
        "fixes": [{
            "fix_id": "MainVarAttrFix",
            "source": {
                "name": "esmvaltool",
                "version": "2.0.0",
                "comments": "",
                "url": "https://github.com/ESMValGroup/ESMValCore/blob/master/esmvalcore/cmor/_fixes/cmip5/hadgem2_cc.py#L34-L55"}
        }]
    }]

    generate_proposals.get_fix_prop_store = Mock(return_value=prop_store)

    with pytest.raises(KeyError) as exc:
        generate_proposals.generate_fix_proposals(file)
    assert exc.value.args[0] == "Required fields not provided: {'operands'}"


def teardown_module():
    # pass
    clear_store()
