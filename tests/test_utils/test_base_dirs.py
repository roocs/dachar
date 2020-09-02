import os
import subprocess

import pytest

from dachar.scan.scan import scan_datasets
from dachar import CONFIG

@pytest.mark.skip("Fails - not possible locally")
def test_c3s_cmip5_base_dir():
    """ Checks definition of c3s cmip5 base dir resolves to a real directory"""
    c3s_cmip5_id = [
        "c3s-cmip5.output1.MOHC.HadGEM2-ES.rcp85.mon.atmos.Amon.r1i1p1.tas.latest"
    ]
    result = scan_datasets(
        project="c3s-cmip5",
        ds_ids=c3s_cmip5_id,
        paths=CONFIG['project:c3s-cmip5']['base_dir'],
        mode="quick",
        location="ceda",
    )

    assert os.path.exists(
        "./outputs/register/c3s-cmip5/output1/MOHC/HadGEM2-ES/rcp85/mon/atmos/Amon.r1i1p1.tas.latest.json"
    )


@pytest.mark.skip("FAILS - c3s-cmip6 base dir not defined yet")
def test_c3s_cmip6_base_dir():
    """ Checks definition of c3s cmip6 base dir resolves to a real directory"""
    c3s_cmip6_id = [
        "c3s-cmip6.CMIP.MOHC.HadGEM3-GC31-LL.amip.r1i1p1f3.Emon.rls.gn.latest"
    ]
    result = scan_datasets(
        project="c3s-cmip6",
        ds_ids=c3s_cmip6_id,
        paths=CONFIG['project:c3s-cmip6']['base_dir'],
        mode="quick",
        location="ceda",
    )
    assert os.path.exists(
        "./outputs/register/c3s-cmip6/CMIP/MOHC/HadGEM3-GC31-LL/amip/r1i1p1f3/Emon.rls.gn.latest.json"
    )


@pytest.mark.skip("Fails - not possible locally")
def test_c3s_cordex_base_dir():
    """ Checks definition of c3s cordex base dir resolves to a real directory"""
    c3s_cordex_id = [
        "c3s-cordex.output.EUR-11.CNRM.CNRM-CERFACS-CNRM-CM5.rcp45.r1i1p1.CNRM-ALADIN53.v1.day.tas.v20150127"
    ]
    result = scan_datasets(
        project="c3s-cordex",
        ds_ids=c3s_cordex_id,
        paths=CONFIG['project:c3s-cordex']['base_dir'],
        mode="quick",
        location="ceda",
    )
    assert os.path.exists(
        "./outputs/register/c3s-cordex/output/EUR-11/CNRM/CNRM-CERFACS-CNRM-CM5/rcp45/r1i1p1/CNRM-ALADIN53/v1.day.tas.v20150127.json"
    )
