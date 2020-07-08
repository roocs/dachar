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
    file_name = fpath.split("/")[-1]
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
    :raises: Raises Inconsistency error if the variable isn't in the file
    """
    ds = Dataset(file)

    if var_id not in ds.variables:
        raise InconsistencyError(
            f"[ERROR] Main variable does not exist in all files. "
            f"Error in file {file}"
        )
    ds.close()


def compare_var_attrs(compare_file, file, var_id):
    """
    Compares the attributes of the given variable across a comparison file and a given file.
    Raises an error if they are not consistent.

    :param compare_file: The file to compare against.
    :param file: The file to carry out the check on.
    :param var_id: The variable to check the attributes of.
    :raises: Raises Inconsistency error if the variable attributes differ
    """
    compare_dict = extract_var_attrs(compare_file, var_id)
    var_dict = extract_var_attrs(file, var_id)

    for key in keys_to_check:
        if key in compare_dict:

            if compare_dict[key] != var_dict[key]:
                raise InconsistencyError(
                    f"[ERROR] Variable attributes for variable {var_id} are not consistent across all files. "
                    f"Could not scan. Inconsistent attribute: {key}"
                )


def get_coords(file, var_id):
    """
    Gets a list of the variable coordinates of a given file excluding the main
    variable and the time variables.

    :param file: The file to extract the variable coordinates from.
    :param var_id: The variable id of the main variable of the file.
    :return: A list of the variable coordinates excluding those related to time.
    """
    ds = Dataset(file)
    coords = []

    for variable in ds.variables:
        if variable != var_id and variable not in ["time", "time_bnds"]:
            coords.append(variable)
    ds.close()

    return coords


def compare_coord_vars(compare_file, file, coords):
    """
    Compares the attributes and the values of the coordinate variables

    :param compare_file: The file to compare against
    :param file: The file to carry out the checks on
    :param coords: The list of coordinates to check
    :raises: Raises Inconsistency error if the variable coordinates differ
    """
    # compare coord attributes
    for coord in coords:
        compare_var_attrs(compare_file, file, coord)
        # compare coord values
        compare_ds = Dataset(compare_file)
        ds = Dataset(file)

        if (compare_ds.variables[coord][:] != ds.variables[coord][:]).any():
            raise InconsistencyError(
                f"[ERROR] Coordinate variables values are not consistent across all files. "
                f"Could not scan. Inconsistent coordinate: {coord}"
            )
        compare_ds.close()
        ds.close()


def convert_to_dss(file_paths):
    """
    Converts a list of netCDF file paths into a list of netCDF dataset objects

    :param file_paths: list of files paths of the netCDF files
    :return: A list of netCDF dataset objects
    """
    datasets = []

    for fpath in file_paths:
        datasets.append(Dataset(fpath))

    return datasets


def check_time(file_paths):
    """
    Uses time-checks to check that there is temporal continuity
    between the file names and the contents of the files.

    :param file_paths: list of files paths of the netCDF files to check
    :raises: Raises Inconsistency error if the time check fails
    """
    # use time-checker
    datasets = convert_to_dss(file_paths)
    result, err = check_multifile_temporal_continuity(datasets, time_index_in_name=-1)

    if result is not True:
        raise InconsistencyError(f"[ERROR] {err}")


def check_files(file_paths):
    """
    Carries out multiple checks on a list of netCDF files to check their
    consistency in attributes, values and temporal continuity before scanning.

    :param file_paths: List of file paths to be scanned
    :raises: Raises Inconsistency error if there are any inconsistencies which
    prevent scanning
    """
    if len(file_paths) <= 1:
        return True

    compare_file = file_paths[0]
    var_id = extract_var_id(compare_file)
    coords = get_coords(compare_file, var_id)
    check_var_id_exists(compare_file, var_id)

    for file in file_paths[1:]:
        check_var_id_exists(file, var_id)
        compare_var_attrs(compare_file, file, var_id)
        compare_coord_vars(compare_file, file, coords)
        compare_var_attrs(compare_file, file, "time")
        compare_var_attrs(compare_file, file, "time_bnds")

    check_time(file_paths)
