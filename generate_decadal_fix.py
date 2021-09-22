"""
To use this script:

In dachar directory:

python generate_decadal_fix.py -f /path/to/file.json -d CMIP6.DCPP.MOHC.HadGEM3-GC31-MM.dcppA-hindcast.s2004-r3i1p1f2.Amon.pr.gn.v20200417 -t 2004-11-01T00:00:00

will generate a fix template at '/path/to/file.json' for the dataset id "CMIP6.DCPP.MOHC.HadGEM3-GC31-MM.dcppA-hindcast.s2004-r3i1p1f2.Amon.pr.gn.v20200417" using the default time 2004-11-01T00:00:00

if -t is not provided, the year will be taken from the ds id if possible, and the date will be YYYY-11-01T00:00:00

"""
import argparse
import json
import re
from datetime import datetime

import cf_xarray
import numpy as np
import xarray as xr
from roocs_utils.project_utils import dsid_to_datapath


def arg_parse():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-f", "--fpath", type=str, required=True, help="Path to output fix json file to"
    )

    parser.add_argument(
        "-d", "--dsid", type=str, required=True, help="ds id to create fix tempalte for"
    )

    parser.add_argument(
        "-t",
        "--time-default",
        type=str,
        required=False,
        help="The default time to use for reftime, startdate and sub experiment id in the format 1986-11-01T00:00:00. If not provided the date will be taken from the ds id if possible",
    )

    return parser.parse_args()


decadal_template = {
    "dataset_id": "",
    "fixes": [
        {
            "fix_id": "VarAttrFix",
            "operands": {"var_id": "time", "attrs": {"long_name": "valid_time"}},
            "source": {
                "name": "ceda",
                "version": "",
                "comments": "",
                "url": "https://github.com/cp4cds/c3s34g_master/tree/master/Decadal",
            },
        },
        {
            "fix_id": "GlobalAttrFix",
            "operands": {
                "attrs": {
                    "forcing_description": "Free text describing the forcings",
                    "physics_description": "Free text describing the physics method",
                    "initialization_description": "Free text describing the initialization method",
                    "startdate": "",
                    "sub_experiment_id": "",
                }
            },
            "source": {
                "name": "ceda",
                "version": "",
                "comments": "",
                "url": "https://github.com/cp4cds/c3s34g_master/tree/master/Decadal",
            },
        },
        {
            "fix_id": "AddScalarCoordFix",
            "operands": {
                "var_id": "reftime",
                "value": "",
                "dtype": "datetime64[ns]",
                "attrs": {
                    "long_name": "Start date of the forecast",
                    "standard_name": "forecast_reference_time",
                },
                "encoding": {
                    "dtype": "int32",
                    "units": "days since 1850-01-01",
                    "calendar": "gregorian",
                },
            },
            "source": {
                "name": "ceda",
                "version": "",
                "comments": "",
                "url": "https://github.com/cp4cds/c3s34g_master/tree/master/Decadal",
            },
        },
        {
            "fix_id": "AddCoordFix",
            "operands": {
                "var_id": "leadtime",
                "value": "",
                "dim": ["time"],
                "dtype": "timedelta64[D]",
                "attrs": {
                    "long_name": "Time elapsed since the start of the forecast",
                    "standard_name": "forecast_period",
                },
                "encoding": {"dtype": "double"},
            },
            "source": {
                "name": "ceda",
                "version": "",
                "comments": "",
                "url": "https://github.com/cp4cds/c3s34g_master/tree/master/Decadal",
            },
        },
        {
            "fix_id": "AddDataVarFix",
            "operands": {
                "var_id": "realization",
                "value": "1",
                "dtype": "int32",
                "attrs": {
                    "long_name": "realization",
                    "comment": "For more information on the ripf, refer to the variant_label, initialization_description, physics_description and forcing_description global attributes",
                },
            },
            "source": {
                "name": "ceda",
                "version": "",
                "comments": "",
                "url": "https://github.com/cp4cds/c3s34g_master/tree/master/Decadal",
            },
        },
        {
            "fix_id": "RemoveFillValuesFix",
            "operands": {},
            "source": {
                "name": "ceda",
                "version": "",
                "comments": "",
                "url": "https://github.com/cp4cds/c3s34g_master/tree/master/Decadal",
            },
        },
        {
            "fix_id": "RemoveCoordAttrFix",
            "operands": {"var_ids": ""},
            "source": {
                "name": "ceda",
                "version": "",
                "comments": "",
                "url": "https://github.com/cp4cds/c3s34g_master/tree/master/Decadal",
            },
        },
    ],
}


def get_reftime(ds, default=None):
    if not default:
        raise Exception(
            "default date must be provided in the format YYYY-MM-DDThh:mm:ss"
        )

    # get the start date

    start_date = ds.attrs.get("startdate", None)

    if not start_date:
        start_date = default

    else:
        #  attempt to get from startdate attribute - don't know if it will always be in sYYYYMM format?
        regex = re.compile(r"^s(\d{4})(\d{2})$")
        match = regex.match(start_date)

        default = datetime.fromisoformat(default)

        if match:
            items = match.groups()
            try:
                start_date = datetime(
                    int(items[0]),
                    int(items[1]),
                    default.day,
                    default.hour,
                    default.minute,
                    default.second,
                ).isoformat()
            except ValueError:
                start_date = default.isoformat()

        else:
            start_date = default.isoformat()

    return start_date


def get_lead_times(ds, start_date):
    times = ds.time.values.astype("datetime64[ns]")
    reftime = np.datetime64(start_date)
    lead_times = []

    # calculate leadtime from reftime and valid times
    for time in times:
        td = time - reftime
        days = td.astype("timedelta64[D]")
        days = int(days.astype(int) / 1)
        lead_times.append(days)

    # put the lead times into a string format
    lts = ""
    for lt in lead_times:
        lts += f"{lt},"

    return lts.rstrip(",")


def get_bnds_variables(ds):
    bnd_vars = ["latitude", "longitude", "time"]
    bounds_list = [ds.cf.get_bounds(bv).name for bv in bnd_vars]
    return bounds_list


def main():
    args = arg_parse()

    fpath = args.fpath
    ds_id = args.dsid

    default = args.time_default

    if not default:
        year = ds_id.split(".")[5].split("-")[0].lstrip("s")
        default = datetime(int(year), 11, 1, 0, 0).isoformat()

    data_path = dsid_to_datapath(ds_id)

    # open dataset
    ds = xr.open_mfdataset(
        f"{data_path}/*.nc",
        use_cftime=True,
        combine="by_coords",
        decode_timedelta=False,
    )

    # get startdate/ subexperiment id
    sd = datetime.fromisoformat(default)
    start_date = f"s{sd.year}{sd.month}"

    # get reftime and lead times
    reftime = get_reftime(ds, default=default)
    lead_times = get_lead_times(ds, sd)

    # put into template
    decadal_template["dataset_id"] = ds_id
    decadal_template["fixes"][1]["operands"]["attrs"]["startdate"] = start_date
    decadal_template["fixes"][1]["operands"]["attrs"]["sub_experiment_id"] = start_date

    # put the reftime in
    decadal_template["fixes"][2]["operands"]["value"] = reftime

    # put the leadtimes in
    decadal_template["fixes"][3]["operands"]["value"] = lead_times

    # put variable names in to remove coordinates attribute from
    bounds_list = get_bnds_variables(ds)
    bounds_list.append("realization")
    decadal_template["fixes"][6]["operands"]["var_ids"] = bounds_list

    # save the template as a json file
    with open(fpath, "w") as fp:
        json.dump(decadal_template, fp, indent=4)


if __name__ == "__main__":
    main()
