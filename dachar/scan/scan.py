#!/usr/bin/env python
"""
Takes arguemnts from the command line and scans each dataset to extract the characteristics.
Outputs the characteristics to JSON files.

Can be re-run if errors are fixed and will only run those which failed.
"""
import collections
import glob
import json
import os

from dachar import config
from dachar.utils import options
from dachar.utils import switch_ds
from dachar.utils.character import extract_character


def to_json(character, output_path):
    """
    Outputs the extracted characteristics to a JSON file.
    If the characteristics can't be output an error file is produced.

    :param character: (dict) The extracted characteristics.
    :param output_path: (string) The file path at which the JSON file is produced.
    :return : None
    """
    # Output to JSON file
    with open(output_path, "w") as writer:
        json.dump(character, writer, indent=4, sort_keys=True)


def _get_ds_paths_from_paths(paths, project):
    """
    Return an OrderedDict of {<ds_id>: <ds_path>} found under the paths provided
    as `paths` (a sequence of directory/file paths).

    :param paths: (sequence) directory/file paths
    :param project: top-level project, e.g. "cmip5", "cmip6" or "cordex" (case-insensitive)
    :return: OrderedDict of {<ds_id>: <ds_path>}
    """
    base_dir = options.project_base_dirs[project]

    # Check paths first
    bad_paths = []

    for pth in paths:
        if not pth.startswith(base_dir):
            bad_paths.append(pth)

    if bad_paths:
        raise Exception(f"Invalid paths provided: {bad_paths}")

    ds_paths = collections.OrderedDict()

    for pth in paths:

        print(f"[INFO] Searching for datasets under: {pth}")
        facet_order = options.facet_rules[project]
        facets_in_path = pth.replace(base_dir, "").strip("/").split("/")

        facets = {}

        for i, facet_name in enumerate(facet_order):
            if len(facets_in_path) <= i:
                break

            facets[facet_name] = facets_in_path[i]

        # Fix facet version if not set
        if not facets.get("version"):
            facets["version"] = "latest"

        facets_as_path = "/".join([facets.get(_, "*") for _ in facet_order])

        # Remove anything matching "files"
        if "/files" in facets_as_path:
            continue

        # TODO: This is repet code of below. Suggest we create a module/class
        #      to manage all mapping of different args to resolve to ds_paths dictionary, later.
        pattern = os.path.join(base_dir, facets_as_path)
        print(f"[INFO] Finding dataset paths for pattern: {pattern}")

        for ds_path in glob.glob(pattern):
            dsid = switch_ds.switch_ds(project, ds_path)
            ds_paths[dsid] = ds_path

    return ds_paths


def get_dataset_paths(project, ds_ids=None, paths=None, facets=None, exclude=None):
    """
    Converts the input arguments into an Ordered Dictionary of {DSID: directory} items.

    :param project: top-level project, e.g. "cmip5", "cmip6" or "cordex" (case-insensitive)
    :param ds_ids: sequence of dataset identifiers (DSIDs), OR None.
    :param paths: sequence of file paths to scan for NetCDF files under, OR None.
    :param facets: dictionary of facet values to limit the search, OR None.
    :param exclude: list of regular expressions to exclude in file paths, OR None.

    :return: An Ordered Dictionary of {dsid: directory}
    """
    base_dir = options.project_base_dirs[project]
    ds_paths = collections.OrderedDict()

    # If ds_ids is defined then ignore all other arguments and use this list
    if ds_ids:

        for dsid in ds_ids:
            if not dsid:
                continue

            ds_path = switch_ds.switch_ds(project, dsid)
            ds_paths[dsid] = ds_path

    # Else use facets if they exist
    elif facets:

        facet_order = options.facet_rules[project]
        facets_as_path = "/".join([facets.get(_, "*") for _ in facet_order])

        pattern = os.path.join(base_dir, facets_as_path)
        print(f"[INFO] Finding dataset paths for pattern: {pattern}")

        for ds_path in glob.glob(pattern):
            dsid = switch_ds.switch_ds(project, ds_path)
            ds_paths[dsid] = ds_path

    elif paths:

        ds_paths = _get_ds_paths_from_paths(paths, project)

    else:
        raise NotImplementedError(
            'Code currently breaks if not using "ds_ids" argument.'
        )

    return ds_paths


def scan_datasets(
    project, mode, location, ds_ids=None, paths=None, facets=None, exclude=None
):
    """
    Loops over ESGF data sets and scans them for character.

    Scans multiple ESGF Datasets found for a given `project` based on a combination of:
     - ds_ids: sequence of dataset identifiers (DSIDs)
     - paths: sequence of file paths to scan for NetCDF files under
     - facets: dictionary of facet values to limit the search
     - exclude: list of regular expressions to exclude in file paths

    The scanned datasets are characterised and the output is written to a JSON file
    if no errors occurred.

    Keeps track of whether the job was successful or not.
    Produces error files if an error occurs, otherwise produces a success file.

    :param project: top-level project, e.g. "cmip5", "cmip6" or "cordex" (case-insensitive)
    :param ds_ids: sequence of dataset identifiers (DSIDs), OR None.
    :param paths: sequence of file paths to scan for NetCDF files under, OR None.
    :param facets: dictionary of facet values to limit the search, OR None.
    :param exclude: list of regular expressions to exclude in file paths, OR None.
    :param mode: Scanning mode: can be either quick or full. A full scan returns
                 max and min values while a quick scan excludes them. Default is quick.
    :return: Dictionary of {"success": list of DSIDs that were successfully scanned,
                            "failed": list of DSIDs that failed to scan}
    """
    # Keep track of failures
    count = 0
    failure_count = 0

    # Filter arguments to get a set of file paths to DSIDs
    ds_paths = get_dataset_paths(
        project, ds_ids=ds_ids, paths=paths, facets=facets, exclude=exclude
    )

    for ds_id, ds_path in ds_paths.items():
        scanner = scan_dataset(project, ds_id, ds_path, mode, location)

        count += 1
        if scanner is False:
            failure_count += 1

    percentage_failed = (failure_count / float(count)) * 100

    print(
        f"[INFO] COMPLETED. Total count: {count}"
        f", Failure count = {failure_count}. Percentage failed"
        f" = {percentage_failed:.2f}%"
    )


def _get_output_paths(project, ds_id):
    """
    Return a dictionary of output paths to write JSON output, success and failure files to.
    Make each parent directory of not already there.

    :param project: top-level project.
    :param ds_id: Dataset Identifier (DSID)
    :return: dictionary of output paths with keys:
             'success', 'json', 'no_files_error', 'extract_error', 'write_error', 'batch'
    """
    grouped_ds_id = switch_ds.get_grouped_ds_id(ds_id)

    paths = {
        "json": config.JSON_OUTPUT_PATH.format(**vars()),
        "no_files_error": config.NO_FILES_PATH.format(**vars()),
        "extract_error": config.EXTRACT_ERROR_PATH.format(**vars()),
        "write_error": config.WRITE_ERROR_PATH.format(**vars()),
        "batch": config.BATCH_OUTPUT_PATH.format(**vars()),
    }

    # Make directories if not already there
    for pth in paths.values():
        dr = os.path.dirname(pth)

        if not os.path.isdir(dr):
            os.makedirs(dr)

    return paths


def analyse_facets(project, ds_id):
    """

    :param project:
    :param ds_id:
    :return:
    """
    facet_names = options.facet_rules[project]
    facet_values = ds_id.split(".")

    return dict(zip(facet_names, facet_values))


def is_registered(json_path):
    if os.path.exists(json_path):
        return True
    else:
        return False


def _check_for_min_max(json_path):
    data = json.load(open(json_path))
    mx = data["data"]["max"]
    mn = data["data"]["min"]
    if mx and mn:
        return True
    else:
        return False


def scan_dataset(project, ds_id, ds_path, mode, location):
    """
    Scans a set of files found under the `ds_path`.

    The scanned datasets are characterised and the output is written to a JSON file
    if no errors occurred.

    Keeps track of whether the job was successful or not.
    Produces error files if an error occurs, otherwise produces a success file.

    :param project: top-level project, e.g. "cmip5", "cmip6" or "cordex" (case-insensitive)
    :param ds_id: dataset identifier (DSID)
    :param ds_path: directory under which to scan data files.
    :param mode: Scanning mode: can be either quick or full. A full scan returns
                 max and min values while a quick scan excludes them. Defaults to quick.'
    :return: Boolean - indicating success of failure of scan.
    """

    if project not in options.known_projects:
        raise Exception(
            f"Project must be one of known projects: {options.known_projects}"
        )

    print(f"[INFO] Scanning dataset: {ds_id}\n\t\t{ds_path} in {mode} mode ")
    facets = analyse_facets(project, ds_id)

    # Generate output file paths
    outputs = _get_output_paths(project, ds_id)

    # check json file exists
    registration = is_registered(outputs["json"])
    if registration:
        try:
            # if json file exists get mode
            data = json.load(open(outputs["json"]))
            mode = data["scan_metadata"]["mode"]
            if mode == "quick":
                print(f"[INFO] Already ran for: {ds_id} in quick mode")
                return True

            if mode == "full":
                check = _check_for_min_max(outputs["json"])
                if check:
                    print(f"[INFO] Already ran for: {ds_id} in full mode")
                    return True

        # flag that a corrupt JSON file exists
        except json.decoder.JSONDecodeError as exc:
            os.remove(outputs["json"])
            print(f"[INFO] Corrupt JSON file. Deleting and re-running.")

    # Delete previous failure files and log files
    for file_key in ("no_files_error", "extract_error", "write_error"):

        err_file = outputs[file_key]
        if os.path.exists(err_file):
            os.remove(err_file)

    # Get data files
    nc_files = glob.glob(f"{ds_path}/*.nc")

    if not nc_files:
        print(f"[ERROR] No data files found for: {ds_path}/*.nc")
        open(outputs["no_files_error"], "w")
        return False

    # Open files with Xarray and get character
    expected_facets = options.facet_rules[project]
    var_id = options.get_facet("variable", facets, project)

    character = extract_character(
        nc_files, location, var_id=var_id, mode=mode, expected_attrs=expected_facets
    )

    try:
        character = extract_character(
            nc_files, location, var_id=var_id, mode=mode, expected_attrs=expected_facets
        )
    except Exception as exc:
        print(f"[ERROR] Could not load Xarray Dataset for: {ds_path}")
        print(f"[ERROR] Files: {nc_files}")
        print(f"[ERROR] Exception was: {exc}")

        # Create error file if can't open dataset
        with open(outputs["extract_error"], "w") as writer:
            writer.write(str(exc))

        return False

    # Output to JSON file
    try:
        output = to_json(character, outputs["json"])
    except Exception as exc:
        print(f'[ERROR] Could not write JSON output: {outputs["json"]}')
        # Create error file if can't output file
        open(outputs["write_error"], "w")
        return False

    print(f'[INFO] Wrote JSON file: {outputs["json"]}')
