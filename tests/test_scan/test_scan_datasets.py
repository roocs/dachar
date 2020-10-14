import json
import pytest
import os
import xarray as xr

from dachar.scan.scan import scan_datasets
from dachar.utils import switch_ds
from dachar import CONFIG, logging
from .test_check_files import make_nc_modify_var_attr

LOGGER = logging.getLogger(__file__)

test_files = [
    "tests/mini-esgf-data/test_data/badc/cmip5/data/cmip5/output1/MOHC/HadGEM2-ES/rcp85/mon/atmos/Amon/r1i1p1/latest/tas/tas_Amon_HadGEM2-ES_rcp85_r1i1p1_200512-203011.nc",
    "tests/mini-esgf-data/test_data/badc/cmip5/data/cmip5/output1/MOHC/HadGEM2-ES/rcp85/mon/atmos/Amon/r1i1p1/latest/tas/tas_Amon_HadGEM2-ES_rcp85_r1i1p1_203012-205511.nc",
    "tests/mini-esgf-data/test_data/badc/cmip5/data/cmip5/output1/MOHC/HadGEM2-ES/rcp85/mon/atmos/Amon/r1i1p1/latest/tas/tas_Amon_HadGEM2-ES_rcp85_r1i1p1_205512-208011.nc",
]

F1, F2, F3 = test_files


class TestCorruptJson:

    def test_fake_corrupt_json_file(self, tmpdir):
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


class TestFileChecker:
    def change_fpath_of_test_file(self, fpath, new_path):
        fname = fpath.split("/")[-1]
        ds = xr.open_mfdataset(fpath, use_cftime=True, combine="by_coords")
        if not os.path.exists(new_path):
            os.makedirs(new_path)
        ds.to_netcdf(path=os.path.join(new_path, f"{fname}"))
        tmp_path = f"{new_path}{fname}"
        return tmp_path

    @pytest.mark.skip("file checker must be uncommented in scan.py")
    # base path for output files must be './outputs'
    def test_file_checker(self):
        path = "tests/test_outputs/cmip5/output1/MOHC/HadGEM2-ES/rcp85/mon/atmos/Amon/r1i1p1/latest/tas/"
        for file in F1, F2:
            self.change_fpath_of_test_file(file, path)
        make_nc_modify_var_attr(F2, "tas", "units", "rubbish", path=path)
        ds_id = ["cmip5.output1.MOHC.HadGEM2-ES.rcp85.mon.atmos.Amon.r1i1p1.latest.tas"]

        grouped_ds_id = switch_ds.get_grouped_ds_id(ds_id[0])
        CONFIG['project:cmip5']['base_dir'] = "tests/test_outputs/"

        failure_file = f"outputs/logs/failure/pre_extract_error/{grouped_ds_id}.log"
        json_file = f"outputs/logs/register/{grouped_ds_id}.json"

        if os.path.exists(failure_file):
            os.unlink(failure_file)
        if os.path.exists(json_file):
            os.unlink(json_file)

        scan_datasets(
            project="cmip5",
            ds_ids=ds_id,
            paths=CONFIG['project:cmip5']['base_dir'],
            mode="quick",
            location="ceda",
        )

        assert os.path.exists(failure_file)
