from dachar import CONFIG
from tests._common import MINI_ESGF_CACHE_DIR


def test_get_from_config():
    path = CONFIG["project:cmip5"]["base_dir"]
    assert path == f"{MINI_ESGF_CACHE_DIR}/master/test_data/badc/cmip5/data"


def test_project_dirs_no_env_var():
    assert (
        CONFIG["project:cmip5"]["base_dir"]
        == f"{MINI_ESGF_CACHE_DIR}/master/test_data/badc/cmip5/data"
    )
    assert (
        CONFIG["project:cmip6"]["base_dir"]
        == f"{MINI_ESGF_CACHE_DIR}/master/test_data/badc/cmip6/data"
    )
    assert (
        CONFIG["project:cordex"]["base_dir"]
        == f"{MINI_ESGF_CACHE_DIR}/master/test_data/badc/cordex/data"
    )
    assert (
        CONFIG["project:c3s-cmip5"]["base_dir"]
        == f"{MINI_ESGF_CACHE_DIR}/master/test_data/gws/nopw/j04/cp4cds1_vol1/data/"
    )
    assert (
        CONFIG["project:c3s-cmip6"]["base_dir"]
        == f"{MINI_ESGF_CACHE_DIR}/master/test_data/badc/cmip6/data"
    )
    assert (
        CONFIG["project:c3s-cordex"]["base_dir"]
        == f"{MINI_ESGF_CACHE_DIR}/master/test_data/gws/nopw/j04/cp4cds1_vol1/data/"
    )
