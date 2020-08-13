import glob
import json
import os
import subprocess
import sys

import numpy as np
import pytest
import xarray as xr

from dachar.scan import scan
from dachar.utils import character
from tests._common import get_tests_project_base_dir


base_dir = get_tests_project_base_dir("cmip5")


# def test_parser():
#     sys.argv = "scan.py -m MOHC/HadGEM2-ES -exp historical -e r1i1p1 -v rh".split()
#     args = scan.arg_parse()
#     for model in args.model:
#         assert model == "MOHC/HadGEM2-ES"
#     for experiment in args.experiment:
#         assert experiment == "historical"
#     for ensemble in args.ensemble:
#         assert ensemble == "r1i1p1"
#     for variable in args.var_id:
#         assert variable == "rh"
#
#
# def test_get_files():
#     model = "MOHC/HadGEM2-ES"
#     experiment = "historical"
#     ensemble = "r1i1p1"
#     var_id = "rh"
#
#     nc_files = scan.find_files(model, experiment, ensemble, var_id)
#     assert nc_files == [
#         "/badc/cmip5/data/cmip5/output1/MOHC/HadGEM2-ES/historical/mon/land/"
#         "Lmon/r1i1p1/latest/rh/rh_Lmon_HadGEM2-ES_historical_r1i1p1_185912-188411.nc",
#         "/badc/cmip5/data/cmip5/output1/MOHC/HadGEM2-ES/historical/mon/land/"
#         "Lmon/r1i1p1/latest/rh/rh_Lmon_HadGEM2-ES_historical_r1i1p1_188412-190911.nc",
#         "/badc/cmip5/data/cmip5/output1/MOHC/HadGEM2-ES/historical/mon/land/"
#         "Lmon/r1i1p1/latest/rh/rh_Lmon_HadGEM2-ES_historical_r1i1p1_190912-193411.nc",
#         "/badc/cmip5/data/cmip5/output1/MOHC/HadGEM2-ES/historical/mon/land/"
#         "Lmon/r1i1p1/latest/rh/rh_Lmon_HadGEM2-ES_historical_r1i1p1_193412-195911.nc",
#         "/badc/cmip5/data/cmip5/output1/MOHC/HadGEM2-ES/historical/mon/land/"
#         "Lmon/r1i1p1/latest/rh/rh_Lmon_HadGEM2-ES_historical_r1i1p1_195912-198411.nc",
#         "/badc/cmip5/data/cmip5/output1/MOHC/HadGEM2-ES/historical/mon/land/"
#         "Lmon/r1i1p1/latest/rh/rh_Lmon_HadGEM2-ES_historical_r1i1p1_198412-200511.nc",
#     ]
#
#
# def test_extract_characteristics_no_error(tmpdir):
#     model = "MOHC/HadGEM2-ES"
#     experiment = "historical"
#     ensemble = "r1i1p1"
#     var_id = "rh"
#
#     nc_files = scan.find_files(model, experiment, ensemble, var_id)
#     ds = xr.open_mfdataset(nc_files)
#     extract_error_path = tmpdir.mkdir("test_extract_error")
#
#     characteristics = lib.character.extract_character(ds, extract_error_path, var_id)
#
#     assert len(characteristics) == 28
#
#
# def test_extract_characteristics_with_error(tmpdir, create_netcdf_file):
#     """ Tests correct thing happens when a characteristic can't be extracted"""
#     var_id = "fake"
#
#     ds = xr.open_dataset(create_netcdf_file)
#     extract_error_path = tmpdir.mkdir("test_extract_error")
#
#     characteristics = lib.character.extract_character(ds, extract_error_path, var_id)
#
#     assert characteristics == False
#
#
# def test_output_to_JSON(tmpdir, create_netcdf_file):
#     var_id = "fake"
#
#     ds = xr.open_dataset(create_netcdf_file)
#     characteristics = {
#         "dims": ds.dims
#     }  # dims isn't serializable so should return False
#     output_path = tmpdir.mkdir("test_output")
#     output_error_path = tmpdir.mkdir("test_output_error")
#     json_file_name = "json_test.json"
#
#     JSON = scan.to_json(
#         characteristics, output_path, json_file_name, output_error_path, var_id
#     )
#
#     assert JSON == False
#
#
# def test_already_run_output():
#     # check nothing returned if success file already produced
#     fpath = "ALL_OUTPUTS/cmip5/output1/MOHC/HadGEM2-ES/historical/JSON_outputs/r1i1p1/cmip5.output1.MOHC.HadGEM2-ES.historical.mon.land.Lmon.r1i1p1.latest.rh.json"
#     if os.path.exists(fpath):
#         os.unlink(fpath)
#     cmd = "python scan.py -m MOHC/HadGEM2-ES -exp historical -e r1i1p1 -v rh"
#     subprocess.call(cmd, shell=True)
#     scanner = scan.scan_dataset("MOHC/HadGEM2-ES", "historical", "r1i1p1", "rh")
#     assert scanner is None
#
#     cmd_delete = (
#         "rm -r ALL_OUTPUTS/cmip5/output1/MOHC/HadGEM2-ES/historical/JSON_outputs/r1i1p1/cmip5.output1."
#         "MOHC.HadGEM2-ES.historical.mon.land.Lmon.r1i1p1.latest.rh.json "
#         "ALL_OUTPUTS/cmip5/output1/MOHC/HadGEM2-ES/historical/success_files/r1i1p1/rh.log"
#     )
#     subprocess.call(cmd_delete, shell=True)
#
#
# def test_scan_no_files():
#     # no files for this file path
#     scanner = scan.scan_dataset("MOHC/HadGEM2-ES", "historical", "r1i1p1", "cMisc")
#     assert scanner == False


# def test_loop_over_vars():
#
# def test_scan_extract_error(): # need example of a file that has a characteristic that can't be extracted
#
# def test_scan_output_error(): # need example of a file that has a characteristic that can't be dumped to json file
#
# def test_scan_open_error(): # need example of a file set that can't be opened using mfdataset


@pytest.mark.skip(reason="Expect to be the wrong shape")
def test_varying_coords_example_fail(create_netcdf_file, create_netcdf_file_2):
    """ Tests what happens when opening files as mfdataset for which the coordinates vary """
    ds = xr.open_mfdataset("test/data/*.nc")

    if not ds.temp.shape == (1752, 145, 192):
        raise Exception(
            f"variable is not the correct shape: should be (1752, 145,192) but is {ds.temp.shape}"
        )

    # seems to keep one variable but joins the coordinate lists together


@pytest.mark.skip(reason="Can't test for this shape when using test data")
def test_varying_coords_example_succeed():
    """ Tests what happens when opening files as mfdataset for which the coordinates vary """
    ds = xr.open_mfdataset(
        f"{base_dir}/cmip5/output1/MOHC/HadGEM2-ES/historical/mon/land/Lmon/r1i1p1/latest/rh/*.nc"
    )

    if not ds.rh.shape == (1752, 145, 192):
        raise Exception(
            f"variable is not the correct shape: should be (1752,145,192) but is {ds.rh.shape}"
        )


@pytest.mark.skip(
    reason="Exception was: Cannot compare type 'Timestamp' with type 'DatetimeProlepticGregorian'"
)
def test_time_axis_types_issue():
    nc_files = [
        f"{base_dir}/cmip5/output1/MPI-M/MPI-ESM-LR/rcp45/mon/ocean/Omon/r1i1p1/latest/zostoga"
        "/zostoga_Omon_MPI-ESM-LR_rcp45_r1i1p1_200601-210012.nc",
        f"{base_dir}/cmip5/output1/MPI-M/MPI-ESM-LR/rcp45/mon/ocean/Omon/r1i1p1/latest/zostoga"
        "/zostoga_Omon_MPI-ESM-LR_rcp45_r1i1p1_210101-230012.nc",
    ]

    ds = xr.open_mfdataset(nc_files)
    da = ds["zostoga"]
    tm = da.coords["time"]

    tm.max()

    # opening only second dataset- get warning: SerializationWarning: Unable to decode time axis into full
    # numpy.datetime64 objects, continuing using dummy cftime.datetime objects instead, reason: dates out of range

    # From xarray webiste:
    # One unfortunate limitation of using datetime64[ns] is that it limits the native representation of dates to
    # those that fall between the years 1678 and 2262. When a netCDF file contains dates outside of these
    # bounds, dates will be returned as arrays of cftime.datetime objects and a CFTimeIndex will be used
    # for indexing. CFTimeIndex enables a subset of the indexing functionality of a pandas.DatetimeIndex
    # and is only fully compatible with the standalone version of cftime (not the version packaged with
    # earlier versions netCDF4).


def test_time_axis_types_issue_fix():
    # fix for Exception was: Cannot compare type 'Timestamp' with type 'DatetimeProlepticGregorian'
    # must be using xarray version 0.15

    nc_files = [
        f"{base_dir}/cmip5/output1/MPI-M/MPI-ESM-LR/rcp45/mon/ocean/Omon/r1i1p1/latest/zostoga"
        "/zostoga_Omon_MPI-ESM-LR_rcp45_r1i1p1_200601-210012.nc",
        f"{base_dir}/cmip5/output1/MPI-M/MPI-ESM-LR/rcp45/mon/ocean/Omon/r1i1p1/latest/zostoga"
        "/zostoga_Omon_MPI-ESM-LR_rcp45_r1i1p1_210101-230012.nc",
    ]

    ds = xr.open_mfdataset(nc_files, use_cftime=True, combine="by_coords")
    da = ds["zostoga"]
    tm = da.coords["time"]

    tm.max()


def test_time_max_as_strftime():
    nc_files = [
        f"{base_dir}/cmip5/output1/MPI-M/MPI-ESM-LR/rcp45/mon/ocean/Omon/r1i1p1/latest/zostoga"
        "/zostoga_Omon_MPI-ESM-LR_rcp45_r1i1p1_200601-210012.nc",
        f"{base_dir}/cmip5/output1/MPI-M/MPI-ESM-LR/rcp45/mon/ocean/Omon/r1i1p1/latest/zostoga"
        "/zostoga_Omon_MPI-ESM-LR_rcp45_r1i1p1_210101-230012.nc",
    ]

    ds = xr.open_mfdataset(nc_files, use_cftime=True, combine="by_coords")
    da = ds["zostoga"]
    tm = da.coords["time"]
    data = tm.values
    mx = data.max()
    mx = mx.strftime("%Y-%m-%dT%H:%M:%S")
    return mx


def test_time_max_as_strftime_to_json():
    nc_files = [
        f"{base_dir}/cmip5/output1/MPI-M/MPI-ESM-LR/rcp45/mon/ocean/Omon/r1i1p1/latest/zostoga"
        "/zostoga_Omon_MPI-ESM-LR_rcp45_r1i1p1_200601-210012.nc",
        f"{base_dir}/cmip5/output1/MPI-M/MPI-ESM-LR/rcp45/mon/ocean/Omon/r1i1p1/latest/zostoga"
        "/zostoga_Omon_MPI-ESM-LR_rcp45_r1i1p1_210101-230012.nc",
    ]

    ds = xr.open_mfdataset(nc_files, use_cftime=True, combine="by_coords")
    da = ds["zostoga"]
    tm = da.coords["time"]
    data = tm.values
    mx = data.max()
    mx = mx.strftime("%Y-%m-%dT%H:%M:%S")

    with open("tests/data/max.json", "w") as write_file:
        json.dump({"time_max": mx}, write_file)


# testing NaNs for min and max
# from data : /badc/cmip5/data/cmip5/output1/MOHC/HadGEM2-ES/historical/mon/land/Lmon/r1i1p1/
# latest/rh/rh_Lmon_HadGEM2-ES_historical_r1i1p1_198412-200511.nc


def test_nan_for_value_min_and_max():
    # python scan.py -d cmip5.output1.MRI.MRI-CGCM3.rcp45.mon.ocean.Omon.r1i1p1.latest.zostoga cmip5
    cmd = "python dachar/scan/scan.py -d cmip5.output1.MOHC.HadGEM2-ES.historical.mon.land.Lmon.r1i1p1.latest.rh cmip5"
    subprocess.call(cmd, shell=True)


def test_min_max_reproduce_nan():
    fpath = f"{base_dir}/cmip5/output1/MOHC/HadGEM2-ES/historical/mon/land/Lmon/r1i1p1/latest/rh/*.nc"
    ds = xr.open_mfdataset(fpath, combine="by_coords")
    data = ds.rh.values
    mx = data.max()
    assert np.isnan(mx)


def test_min_max_value():
    fpath = f"{base_dir}/cmip5/output1/MOHC/HadGEM2-ES/historical/mon/land/Lmon/r1i1p1/latest/rh/*.nc"
    ds = xr.open_mfdataset(fpath, combine="by_coords")
    mx = float(ds.rh.max())
    assert np.isfinite(mx)


def teardown_module():
    pass
