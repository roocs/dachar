import configparser
import os
import shutil
import subprocess
import tempfile
import warnings
from unittest.mock import Mock

import pytest

from dachar import CONFIG
from dachar.scan import scan
from tests._stores_for_tests import _TestDatasetCharacterStore

# Must run with --noconftest flag

char_store = None
cwd = os.getcwd()


def clear_store():
    dc_dr = _TestDatasetCharacterStore.config["local.base_dir"]
    if os.path.isdir(dc_dr):
        shutil.rmtree(dc_dr)


def setup_module():
    clear_store()
    global char_store
    char_store = _TestDatasetCharacterStore()


@pytest.mark.xfail(
    reason="conftest overwrites base dire to test base dir. Will pass if run with --noconftest flag"
)
@pytest.mark.skipif(
    os.path.isdir("/group_workspaces") is False, reason="data not available"
)
def test_c3s_cmip5_base_dir():
    """ Checks definition of c3s cmip5 base dir resolves to a real directory"""
    scan.get_dc_store = Mock(return_value=char_store)

    c3s_cmip5_id = [
        "c3s-cmip5.output1.MOHC.HadGEM2-ES.rcp85.mon.atmos.Amon.r1i1p1.tas.latest"
    ]
    scan.scan_datasets(
        project="c3s-cmip5",
        ds_ids=c3s_cmip5_id,
        paths=CONFIG["project:c3s-cmip5"]["base_dir"],
        mode="quick",
        location="ceda",
    )

    assert os.path.exists(
        os.path.join(
            char_store.config.get("local.base_dir"),
            "c3s-cmip5/output1/MOHC/HadGEM2-ES/rcp85/mon/atmos/Amon.r1i1p1.tas.latest.json",
        )
    )


@pytest.mark.xfail(
    reason="conftest overwrites base dire to test base dir. Will pass if run with --noconftest flag"
)
@pytest.mark.skipif(os.path.isdir("/badc") is False, reason="data not available")
def test_c3s_cmip6_base_dir():
    """ Checks definition of c3s cmip6 base dir resolves to a real directory"""
    scan.get_dc_store = Mock(return_value=char_store)

    c3s_cmip6_id = [
        "c3s-cmip6.CMIP.MOHC.HadGEM3-GC31-LL.amip.r1i1p1f3.Emon.rls.gn.latest"
    ]
    scan.scan_datasets(
        project="c3s-cmip6",
        ds_ids=c3s_cmip6_id,
        paths=CONFIG["project:c3s-cmip6"]["base_dir"],
        mode="quick",
        location="ceda",
    )

    # base dir not defined yet
    assert os.path.exists(
        os.path.join(
            char_store.config.get("local.base_dir"),
            "c3s-cmip6/CMIP/MOHC/HadGEM3-GC31-LL/amip/r1i1p1f3/Emon.rls.gn.latest.json",
        )
    )


@pytest.mark.xfail(
    reason="conftest overwrites base dire to test base dir. Will pass if run with --noconftest flag"
)
@pytest.mark.skipif(
    os.path.isdir("/group_workspaces") is False, reason="data not available"
)
def test_c3s_cordex_base_dir():
    """ Checks definition of c3s cordex base dir resolves to a real directory"""
    scan.get_dc_store = Mock(return_value=char_store)

    c3s_cordex_id = [
        "c3s-cordex.output.EUR-11.CNRM.CNRM-CERFACS-CNRM-CM5.rcp45.r1i1p1.CNRM-ALADIN53.v1.day.tas.v20150127"
    ]
    scan.scan_datasets(
        project="c3s-cordex",
        ds_ids=c3s_cordex_id,
        paths=CONFIG["project:c3s-cordex"]["base_dir"],
        mode="quick",
        location="ceda",
    )
    assert os.path.exists(
        os.path.join(
            char_store.config.get("local.base_dir"),
            "c3s-cordex/output/EUR-11/CNRM/CNRM-CERFACS-CNRM-CM5/rcp45/r1i1p1"
            "/CNRM-ALADIN53/v1.day.tas.v20150127.json",
        )
    )


def teardown_module():
    # pass
    clear_store()
