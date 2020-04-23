from netCDF4 import Dataset

from time_checks.multifile_time_checks import check_multifile_temporal_continuity

keys_to_check = ["standard_name", "long_name", "units", "_FillValue", "missing_value"]


class InconsistencyError(Exception):
    """ Raised when there is some inconsistency which prevents files
    being scanned. """


def extract_var_id(fpath):
    # for cmip5 file structure
    file_name = fpath.split("/")[-2]
    var_id = file_name.split("_")[0]
    print(var_id)
    return var_id


def extract_var_attrs(fpath, var_id):
    ds = Dataset(fpath)
    var_dict = dict(
        [
            (attr, getattr(ds.variables[var_id], attr))
            for attr in ds.variables[var_id].ncattrs()
        ]
    )
    ds.close()
    return var_dict


def check_var_id_exists(file, var_id):
    ds = Dataset(file)
    try:
        assert var_id in ds.variables
        ds.close()
    except AssertionError as exc:
        raise InconsistencyError(
            f"[ERROR] Main variable does not exist in all files. "
            f"Error in file {file}"
        )


def compare_var_attrs(compare_file, file, var_id):
    compare_dict = extract_var_attrs(compare_file, var_id)
    var_dict = extract_var_attrs(file, var_id)
    for key in keys_to_check:
        if key in compare_dict:
            try:
                assert compare_dict[key] == var_dict[key]
            except (AssertionError, KeyError) as exc:
                raise InconsistencyError(
                    f"[ERROR] Variable attributes for variable {var_id} are not consistent across all files. "
                    f"Could not scan. Inconsistent attribute: {key}"
                )


def get_coords(file, var_id):
    ds = Dataset(file)
    coords = []
    for variable in ds.variables:
        if variable == var_id:
            continue
        elif variable in ["time", "time_bnds"]:
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
            raise InconsistencyError(
                f"[ERROR] Coordinate variables values are not consistent across all files. "
                f"Could not scan. Inconsistent coordinate: {coord}"
            )


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
        check_var_id_exists(file, var_id)
        compare_var_attrs(compare_file, file, var_id)
        compare_coord_vars(compare_file, file, coords)
        compare_var_attrs(compare_file, file, "time")
        compare_var_attrs(compare_file, file, "time_bnds")
    check_time(file_paths)
