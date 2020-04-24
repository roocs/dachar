from netCDF4 import Dataset

from time_checks.multifile_time_checks import check_multifile_temporal_continuity

keys_to_check = ["standard_name", "long_name", "units", "_FillValue", "missing_value"]


class InconsistencyError(Exception):
    """ Raised when there is some inconsistency which prevents files
    being scanned. """


def extract_var_id(fpath):
    """
    Extract the main variable of the file given by the file path. The variable is extracted
    according to its expected position in the file path.

    :param fpath: The file path of the file to extract the var_id from
    :return: The variable id of the main variable in the given file
    """
    # for cmip5 file structure
    file_name = fpath.split("/")[-2]
    var_id = file_name.split("_")[0]
    return var_id


def extract_var_attrs(fpath, var_id):
    """
    Extract the variable attributes of the given variable and return as a dictionary.

    :param fpath: File path of file to extract the variable attributes from
    :param var_id: Variable to collect attributes from
    :return: A dictionary of the variable attributes
    """
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
    """
    Checks the variable id provided exists in the given file.

    :param file: File to check for variable in
    :param var_id: Variable to check for
    :return:
    """
    ds = Dataset(file)
    if var_id in ds.variables:
        pass
    else:
        print(
            f"[ERROR] Main variable does not exist in all files. "
            f"Error in file {file}"
        )
        return False
    ds.close()

def compare_var_attrs(compare_file, file, var_id):
    """

    :param compare_file:
    :param file:
    :param var_id:
    :return:
    """
    compare_dict = extract_var_attrs(compare_file, var_id)
    var_dict = extract_var_attrs(file, var_id)
    for key in keys_to_check:
        if key in compare_dict:
            if compare_dict[key] == var_dict[key]:
                continue
            else:
                print(f"[ERROR] Variable attributes for variable {var_id} are not consistent across all files. "
                      f"Could not scan. Inconsistent attribute: {key}")
                return False



def get_coords(file, var_id):
    """

    :param file:
    :param var_id:
    :return:
    """
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
    """

    :param compare_file:
    :param file:
    :param coords:
    :return:
    """
    # compare coord attributes
    for coord in coords:
        compare_var_attrs(compare_file, file, coord)
        # compare coord values
        compare_ds = Dataset(compare_file)
        ds = Dataset(file)
        if (compare_ds.variables[coord][:] == ds.variables[coord][:]).all():
            compare_ds.close()
            ds.close()
            continue
        else:
            print(
                f"[ERROR] Coordinate variables values are not consistent across all files. "
                f"Could not scan. Inconsistent coordinate: {coord}"
            )
            return False


def convert_to_dss(file_paths):
    """

    :param file_paths:
    :return:
    """
    """ Converts a list of netcdf file paths into a dictionary of datasets"""
    datasets = []
    for fpath in file_paths:
        datasets.append(Dataset(fpath))
    return datasets


def check_time(file_paths):
    """

    :param file_paths:
    :return:
    """
    # use time-checker
    datasets = convert_to_dss(file_paths)
    result, err = check_multifile_temporal_continuity(datasets, time_index_in_name=-1)
    if result is not True:
        print(f"[ERROR] {err}")
        return False


def check_files(file_paths):
    """

    :param file_paths:
    :return:
    """
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

