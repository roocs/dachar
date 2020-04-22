from netCDF4 import Dataset
import pytest
import os
import xarray as xr
import numpy as np
import itertools

from time_checks.multifile_time_checks import check_multifile_temporal_continuity

test_files = [
    "tests/mini-esgf-data/test_data/badc/cmip5/data/cmip5/output1/MOHC/HadGEM2-ES/rcp85/mon/atmos/Amon/r1i1p1/latest/tas/tas_Amon_HadGEM2-ES_rcp85_r1i1p1_200512-203011.nc",
    "tests/mini-esgf-data/test_data/badc/cmip5/data/cmip5/output1/MOHC/HadGEM2-ES/rcp85/mon/atmos/Amon/r1i1p1/latest/tas/tas_Amon_HadGEM2-ES_rcp85_r1i1p1_203012-205511.nc",
    "tests/mini-esgf-data/test_data/badc/cmip5/data/cmip5/output1/MOHC/HadGEM2-ES/rcp85/mon/atmos/Amon/r1i1p1/latest/tas/tas_Amon_HadGEM2-ES_rcp85_r1i1p1_205512-208011.nc",
]

F1, F2, F3 = test_files

keys_to_check = ['standard_name', 'long_name', 'units', '_FillValue', 'missing_value']


class InconsistencyError(Exception):
    """ Raised when there is some inconsistency which prevents files
    being scanned. """


def extract_var_id(fpath):
    # for cmip5 file structure
    var_id = fpath.split('/')[-2]
    return var_id


def extract_var_attrs(fpath, var_id):
    ds = Dataset(fpath)
    var_dict = dict([(attr, getattr(ds.variables[var_id], attr)) for attr in ds.variables[var_id].ncattrs()])
    ds.close()
    return var_dict


def check_var_id_exists(file, var_id):
    ds = Dataset(file)
    try:
        assert var_id in ds.variables
        ds.close()
    except AssertionError as exc:
        raise InconsistencyError(f'[ERROR] Main variable does not exist in all files. '
                             f'Error in file {file}')


def compare_var_attrs(compare_file, file, var_id):
    compare_dict = extract_var_attrs(compare_file, var_id)
    var_dict = extract_var_attrs(file, var_id)
    for key in keys_to_check:
        if key in compare_dict:
            try:
                assert(compare_dict[key] == var_dict[key])
            except (AssertionError, KeyError) as exc:
                raise InconsistencyError(f'[ERROR] Variable attributes are not consistent across all files. '
                                     f'Could not scan. Inconsistent attribute: {key}')


def get_coords(file, var_id):
    ds = Dataset(file)
    coords = []
    for variable in ds.variables:
        if variable == var_id:
            continue
        elif variable in ['time', 'time_bnds']:
            continue
        else:
            coords.append(variable)
    ds.close()
    return coords


def compare_coord_vars(compare_file, file, coords):
    # compare coord attributes
    for coord in coords:
        compare_var_attrs(compare_file, file, coord)
    # compare coord values
        try:
            compare_ds = Dataset(compare_file)
            ds = Dataset(file)
            assert (compare_ds.variables[coord][:] == ds.variables[coord][:]).all()
            compare_ds.close()
            ds.close()
        except AssertionError as exc:
            raise InconsistencyError(f'[ERROR] Coordinate variables values are not consistent across all files. '
                                 f'Could not scan. Inconsistent coordinate: {coord}')


def convert_to_dss(file_paths):
    """ Converts a list of netcdf file paths into a dictionary of datasets"""
    datasets = []
    for fpath in file_paths:
        datasets.append(Dataset(fpath))
    return datasets


def check_time(file_paths):
    # use time-checker
    datasets = convert_to_dss(file_paths)
    result, err = check_multifile_temporal_continuity(datasets, time_index_in_name=-1)
    if result is not True:
        raise InconsistencyError(f"[ERROR] {err}")


def check_files(file_paths):
    compare_file = file_paths[0]
    var_id = extract_var_id(compare_file)
    coords = get_coords(compare_file, var_id)
    for file in file_paths:
        try:
            check_var_id_exists(file, var_id)
            compare_var_attrs(compare_file, file, var_id)
            compare_var_attrs(compare_file, file, 'time')
            compare_var_attrs(compare_file, file, 'time_bnds')
            compare_coord_vars(compare_file, file, coords)
        except Exception as exc:
            raise
    check_time(file_paths)


def _open(file_paths):
    return xr.open_mfdataset(
        file_paths, use_cftime=True, combine="by_coords", compat="equals"
    )


def _check_and_open(file_paths):
    check_files(file_paths)
    return xr.open_mfdataset(
        file_paths, use_cftime=True, combine="by_coords", compat="equals"
    )


def _make_nc_modify_var_attr(nc_path, var_id, attr, value):
    ds = _open(nc_path)
    ds[var_id].attrs[attr] = value
    path = "tests/test_outputs/tas/"
    if not os.path.exists(path):
        os.makedirs(path)
    ds.to_netcdf(path=os.path.join(path, "modify_var_attr.nc"))
    tmp_path = os.path.abspath(path+"modify_var_attr.nc")
    return tmp_path


def _make_nc_modify_var_id(nc_path, old_var_id, new_var_id):
    ds = _open(nc_path)
    ds = ds.rename({old_var_id: new_var_id})
    path = "tests/test_outputs/tas/"
    if not os.path.exists(path):
        os.makedirs(path)
    ds.to_netcdf(path=os.path.join(path, "modify_var_id.nc"))
    tmp_path = os.path.abspath(path+"modify_var_id.nc")
    return tmp_path


def _make_nc_modify_fill_value(nc_path, var_id, fill_value):
    ds = _open(nc_path)
    ds[var_id].encoding["_FillValue"] = fill_value
    ds.tas.encoding["missing_value"] = fill_value
    path = "tests/test_outputs/tas/"
    if not os.path.exists(path):
        os.makedirs(path)
    ds.to_netcdf(path=os.path.join(path,"modify_fill_value.nc"))
    tmp_path = os.path.abspath(path+"modify_fill_value.nc")
    return tmp_path


@pytest.fixture(params=["units", "standard_name", "long_name"])
def var_attr(request):
    attr = request.param
    return attr


def test_agg_success_with_no_changes():
    ds_open = _open([F1, F2, F3])
    ds_check = _check_and_open([F1, F2, F3])
    assert ds_open == ds_check


def test_agg_fails_diff_var_attrs(var_attr):
    V = "rubbish"
    file_paths = F1, _make_nc_modify_var_attr(F2, "tas", var_attr, V), F3
    try:
        _check_and_open(file_paths)
    except InconsistencyError as exc:
        assert (
            str(exc)
            == f"[ERROR] Variable attributes are not consistent across all files. "
               f"Could not scan. Inconsistent attribute: {var_attr}"
        )


def test_agg_fails_diff_var_id():
    new_var_id = "blah"
    old_var_id = "tas"
    file_paths = _make_nc_modify_var_id(F1, old_var_id, new_var_id), F2, F3
    try:
        _check_and_open(file_paths)
    except InconsistencyError as exc:
        assert (
            str(exc)
            == "[ERROR] Main variable does not exist in all files. Error in file /Users/qsp95418/roocs/dachar/tests/test_outputs/tas/modify_var_id.nc"
        )


def test_agg_fails_diff_fill_value():
    fill_value = np.float32(-1e20)
    file_paths = F1, _make_nc_modify_fill_value(F2, "tas", fill_value=fill_value), F3
    try:
        _check_and_open(file_paths)
    except InconsistencyError as exc:
        assert (
            str(exc)
            == "[ERROR] Variable attributes are not consistent across all files. Could not scan. Inconsistent attribute: _FillValue"
        )


def test_agg_failures_not_affected_by_order():
    # Apply a breaking change to different files in the sequence and
    # assert that the same exception is raised regardless of which
    # file is modified
    file_orders = itertools.permutations([F1, F2, F3])
    for _f1, _f2, _f3 in file_orders:
        file_paths = _f1, _make_nc_modify_var_attr(_f2, "tas", "units", "bad"), _f3
        try:
            _check_and_open(file_paths)
        except InconsistencyError as exc:
            assert (
                str(exc)
                == "[ERROR] Variable attributes are not consistent across all files. Could not scan. Inconsistent attribute: units"
            )

