import os

from roocs_utils.project_utils import DatasetMapper

from dachar import CONFIG


def get_grouped_ds_id(ds_id):

    # Define a "grouped" ds_id that splits facets across directories and then groups
    # the final set into a file path, based on dir_grouping_level value in CONFIG
    gl = CONFIG["dachar:settings"]["dir_grouping_level"]
    parts = ds_id.split(".")
    grouped_ds_id = "/".join(parts[:-gl]) + "/" + ".".join(parts[-gl:])

    return grouped_ds_id


def switch_ds(project, ds):
    """
    Switches between ds_path and ds_id.

    :param project: top-level project
    :param ds: either dataset path or dataset ID (DSID)
    :return: either dataset path or dataset ID (DSID) - switched from the input.
    """
    if ds.startswith("/"):
        return DatasetMapper(ds, project=project).ds_id
    else:
        return DatasetMapper(ds, project=project).data_path
