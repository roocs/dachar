import os
import mock
from dachar import CONFIG
from tests._common import TESTS_HOME


def test_get_from_config():
    path = CONFIG['project:cmip5']['base_dir']
    assert path == os.path.join(TESTS_HOME, "mini-esgf-data/test_data/badc/cmip5/data")


def test_project_dirs_no_env_var():
    assert CONFIG['project:cmip5']['base_dir'] == os.path.join(TESTS_HOME, "mini-esgf-data/test_data/badc/cmip5/data")
    assert CONFIG['project:cmip6']['base_dir'] == os.path.join(TESTS_HOME, "mini-esgf-data/test_data/badc/cmip6/data")
    assert CONFIG['project:cordex']['base_dir'] == os.path.join(TESTS_HOME, "mini-esgf-data/test_data/badc/cordex/data")
    assert (
        CONFIG['project:c3s-cmip5']['base_dir']
        == os.path.join(TESTS_HOME, "mini-esgf-data/test_data/group_workspaces/jasmin2/cp4cds1/vol1/data")
    )
    assert CONFIG['project:c3s-cmip6']['base_dir'] == "NOT DEFINED YET"
    assert (
        CONFIG['project:c3s-cordex']['base_dir']
        == os.path.join(TESTS_HOME, "mini-esgf-data/test_data/group_workspaces/jasmin2/cp4cds1/vol1/data")
    )




