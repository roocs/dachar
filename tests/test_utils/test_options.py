import os
import mock
from importlib import reload
from dachar.utils import options


def test_project_dirs_no_env_var():
    reload(options)

    assert options.get_project_base_dir("cmip5") == "/badc/cmip5/data"
    assert options.get_project_base_dir("cmip6") == "/badc/cmip6/data"
    assert options.get_project_base_dir("cordex") == "/badc/cordex/data"
    assert (
        options.get_project_base_dir("c3s-cmip5")
        == "/group_workspaces/jasmin2/cp4cds1/vol1/data/"
    )
    assert options.get_project_base_dir("c3s-cmip6") == "NOT DEFINED YET"
    assert (
        options.get_project_base_dir("c3s-cordex")
        == "/group_workspaces/jasmin2/cp4cds1/vol1/data/"
    )


@mock.patch.dict(os.environ, {"ROOCS_CONFIG": "./tests/test_utils/"})
# as environment variable is present, dictionary gets updated with dictionary in config_local file
def test_project_dirs_paths_env_var():
    reload(options)

    assert options.get_project_base_dir("cmip5") == "cmip5/file/path/for/tests"
    assert options.get_project_base_dir("cmip6") == "/badc/cmip6/data"
    assert options.get_project_base_dir("cordex") == "cordex/file/path/for/tests"
    assert options.get_project_base_dir("c3s-cmip5") == "c3s-cmip5/file/path/for/tests"
    assert options.get_project_base_dir("c3s-cmip6") == "c3s-cmip6/file/path/for/tests"
    assert (
        options.get_project_base_dir("c3s-cordex") == "/group_workspaces/jasmin2/cp4cds1/vol1/data/"
    )
