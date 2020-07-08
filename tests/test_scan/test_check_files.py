from netCDF4 import Dataset
import pytest
import os
import xarray as xr
import numpy as np
import itertools

from time_checks.multifile_time_checks import check_multifile_temporal_continuity
from dachar.scan.check_files import check_files, InconsistencyError

test_files = [
    "tests/mini-esgf-data/test_data/badc/cmip5/data/cmip5/output1/MOHC/HadGEM2-ES/rcp85/mon/atmos/Amon/r1i1p1/latest/tas/tas_Amon_HadGEM2-ES_rcp85_r1i1p1_200512-203011.nc",
    "tests/mini-esgf-data/test_data/badc/cmip5/data/cmip5/output1/MOHC/HadGEM2-ES/rcp85/mon/atmos/Amon/r1i1p1/latest/tas/tas_Amon_HadGEM2-ES_rcp85_r1i1p1_203012-205511.nc",
    "tests/mini-esgf-data/test_data/badc/cmip5/data/cmip5/output1/MOHC/HadGEM2-ES/rcp85/mon/atmos/Amon/r1i1p1/latest/tas/tas_Amon_HadGEM2-ES_rcp85_r1i1p1_205512-208011.nc",
]

F1, F2, F3 = test_files


def open(file_paths):
    return xr.open_mfdataset(file_paths, use_cftime=True, combine="by_coords")


def _check_and_open(file_paths):
    check_files(file_paths)
    return xr.open_mfdataset(
        file_paths, use_cftime=True, combine="by_coords", compat="equals"
    )


# if file is tested by time checker - test file needs to have nave in format
# 'var_freq_name_timerange.nc'
# for example: 'tas_Amon_modify_coord_value_203012-205511.nc'
# otherwise test file names need to start with the variable followed by and underscore ('tas_..')

# make files temporary?
def make_nc_modify_var_attr(nc_path, var_id, attr, value, path="tests/test_outputs/"):
    ds = open(nc_path)
    ds[var_id].attrs[attr] = value
    if not os.path.exists(path):
        os.makedirs(path)
    ds.to_netcdf(path=os.path.join(path, "tas_modify_var_attr.nc"))
    tmp_path = os.path.join(path, "tas_modify_var_attr.nc")
    return tmp_path


def make_nc_modify_var_id(nc_path, old_var_id, new_var_id, path="tests/test_outputs/"):
    ds = open(nc_path)
    ds = ds.rename({old_var_id: new_var_id})
    if not os.path.exists(path):
        os.makedirs(path)
    ds.to_netcdf(path=os.path.join(path, "tas_modify_var_id.nc"))
    tmp_path = os.path.join(path, "tas_modify_var_id.nc")
    return tmp_path


def make_nc_modify_fill_value(nc_path, var_id, fill_value, path="tests/test_outputs/"):
    ds = open(nc_path)
    ds[var_id].encoding["_FillValue"] = fill_value
    ds.tas.encoding["missing_value"] = fill_value
    if not os.path.exists(path):
        os.makedirs(path)
    ds.to_netcdf(path=os.path.join(path, "tas_modify_fill_value.nc"))
    tmp_path = os.path.join(path, "tas_modify_fill_value.nc")
    return tmp_path


def make_nc_modify_coord_value(nc_path, path="tests/test_outputs/"):
    ds = open(nc_path)
    # ds['lat'].data = np.ones((2,))
    ds_new = ds.assign_coords(lat=np.ones((2,)))
    # assign coords doesn't copy across attributes as well
    ds_new.lat.attrs = ds.lat.attrs
    if not os.path.exists(path):
        os.makedirs(path)
    ds_new.to_netcdf(path=os.path.join(path, "tas_modify_coord_value.nc"))
    tmp_path = os.path.join(path, "tas_modify_coord_value.nc")
    return tmp_path


@pytest.fixture(params=["units", "standard_name", "long_name"])
def var_attr(request):
    attr = request.param
    return attr


def test_success_with_no_changes():
    ds_open = open([F1, F2, F3])
    ds_check = _check_and_open([F1, F2, F3])
    assert ds_open == ds_check


def test_fail_diff_var_attrs(var_attr):
    V = "rubbish"
    file_paths = F1, make_nc_modify_var_attr(F2, "tas", var_attr, V), F3
    try:
        _check_and_open(file_paths)
    except InconsistencyError as exc:
        assert (
            str(exc)
            == f"[ERROR] Variable attributes for variable tas are not consistent across all files. "
            f"Could not scan. Inconsistent attribute: {var_attr}"
        )


def test_fail_diff_fill_value():
    fill_value = np.float32(-1e20)
    file_paths = F1, make_nc_modify_fill_value(F2, "tas", fill_value=fill_value), F3
    try:
        _check_and_open(file_paths)
    except InconsistencyError as exc:
        assert (
            str(exc)
            == "[ERROR] Variable attributes for variable tas are not consistent across all files. Could not scan. Inconsistent attribute: _FillValue"
        )


def test_fail_diff_var_id():
    new_var_id = "blah"
    old_var_id = "tas"
    _f = make_nc_modify_var_id(F2, old_var_id, new_var_id)
    file_paths = F1, _f, F3
    try:
        _check_and_open(file_paths)
    except InconsistencyError as exc:
        assert (
            str(exc)
            == f"[ERROR] Main variable does not exist in all files. Error in file {_f}"
        )


def test_fail_files_missing_in_time_series():
    # exclude middle file to break up time series
    file_paths = F1, F3
    try:
        _check_and_open(file_paths)
    except InconsistencyError as exc:
        assert str(exc) == "[ERROR] File not in series"


def test_fail_coord_values_different():
    file_paths = F1, make_nc_modify_coord_value(F2), F3
    try:
        _check_and_open(file_paths)
    except InconsistencyError as exc:
        assert (
            str(exc)
            == "[ERROR] Coordinate variables values are not consistent across all files. Could not scan. Inconsistent coordinate: lat"
        )


def test_fail_coord_attr_different():
    V = "fake"
    file_paths = F1, make_nc_modify_var_attr(F2, "lat", "standard_name", V), F3
    try:
        _check_and_open(file_paths)
    except InconsistencyError as exc:
        assert (
            str(exc)
            == f"[ERROR] Variable attributes for variable lat are not consistent across all files. "
            f"Could not scan. Inconsistent attribute: standard_name"
        )


def test_fail_time_attr_different():
    V = "fake"
    file_paths = F1, make_nc_modify_var_attr(F2, "time", "standard_name", V), F3
    try:
        _check_and_open(file_paths)
    except InconsistencyError as exc:
        assert (
            str(exc)
            == f"[ERROR] Variable attributes for variable time are not consistent across all files. "
            f"Could not scan. Inconsistent attribute: standard_name"
        )


def test_failures_not_affected_by_order():
    # Apply a breaking change to different files in the sequence and
    # assert that the same exception is raised regardless of which
    # file is modified
    file_orders = itertools.permutations([F1, F2, F3])
    for _f1, _f2, _f3 in file_orders:
        file_paths = _f1, make_nc_modify_var_attr(_f2, "tas", "units", "bad"), _f3
        try:
            _check_and_open(file_paths)
        except InconsistencyError as exc:
            assert (
                str(exc)
                == "[ERROR] Variable attributes for variable tas are not consistent across all files. Could not scan. Inconsistent attribute: units"
            )
