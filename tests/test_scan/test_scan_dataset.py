import json
import os

import pytest

from dachar.scan.scan import scan_datasets
from dachar import CONFIG
from dachar import logging

LOGGER = logging.getLogger(__file__)


@pytest.mark.skip("This ds id no longer creates a corrupt JSON file")
def test_corrupt_json_file():
    """ Tests what happens when a JSON file exists but is incomplete due to an issue encoding."""
    ds_id = [
        "c3s-cordex.output.EUR-11.IPSL.MOHC-HadGEM2-ES.rcp85.r1i1p1.IPSL-WRF381P.v1.day.psl.v20190212"
    ]
    scan_datasets(
        project="c3s-cordex",
        ds_ids=ds_id,
        paths=CONFIG['project:c3s-cordex']['base_dir'],
        mode="quick",
        location="ceda",
    )
    try:
        scan_datasets(
            project="c3s-cordex",
            ds_ids=ds_id,
            paths=CONFIG['project:c3s-cordex']['base_dir'],
            mode="quick",
            location="ceda",
        )
    except json.decoder.JSONDecodeError as exc:
        pass


def test_fake_corrupt_json_file(tmpdir):
    """ Creates a bad JSON file and tests the code responds properly"""
    try:
        d = tmpdir.mkdir("./testdir")
        bad_json = d.join("bad_json.txt")
        bad_json.write('{"test": }')
        filename = os.path.join(bad_json.dirname, bad_json.basename)
        json.load(open(filename))
    except json.decoder.JSONDecodeError as exc:
        LOGGER.debug(f"Corrupt JSON file found.")
        pass


def teardown_module(module):
    pass
