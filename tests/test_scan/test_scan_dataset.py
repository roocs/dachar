import json
import pytest
import os

from dachar.scan.scan import scan_datasets
from dachar.utils import options


def setup_module(module):
    options.project_base_dirs['c3s-cordex'] = 'tests/mini-esgf-data/test_data/group_workspaces/jasmin2/cp4cds1/data'
    module.base_dir = options.project_base_dirs['c3s-cordex']


@pytest.mark.skip('This ds id no longer creates a corrupt JSON file')
def test_corrupt_json_file():
    """ Tests what happens when a JSON file exists but is incomplete due to an issue encoding."""
    ds_id = ["c3s-cordex.output.EUR-11.IPSL.MOHC-HadGEM2-ES.rcp85.r1i1p1.IPSL-WRF381P.v1.day.psl.v20190212"]
    scan_datasets(project='c3s-cordex', ds_ids=ds_id, paths=options.project_base_dirs['c3s-cordex'],
                  mode='quick', location='ceda')
    try:
        scan_datasets(project='c3s-cordex', ds_ids=ds_id, paths=options.project_base_dirs['c3s-cordex'],
                      mode='quick', location='ceda')
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
        print('[INFO] Corrupt JSON file found.')
        pass


def teardown_module(module):
    options.project_base_dirs['c3s-cordex'] = '/group_workspaces/jasmin2/cp4cds1/data'
    module.base_dir = options.project_base_dirs['c3s-cordex']
