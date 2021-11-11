# -*- coding: utf-8 -*-
"""
To use this script:

In dachar directory:

python generate_decadal_fix.py -f /path/to/file.json -d CMIP6.DCPP.MOHC.HadGEM3-GC31-MM.dcppA-hindcast.s2004-r3i1p1f2.Amon.pr.gn.v20200417

will generate a fix template at '/path/to/file.json' for the dataset id "CMIP6.DCPP.MOHC.HadGEM3-GC31-MM.dcppA-hindcast.s2004-r3i1p1f2.Amon.pr.gn.v20200417"

The year will be taken from the ds id if possible for the start date of the experiment, and  will be YYYY-11-01T00:00:00

"""
import argparse
import copy
import json
import re
from datetime import datetime

import numpy as np
import xarray as xr
from roocs_utils.project_utils import dsid_to_datapath


def arg_parse():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-f", "--fpath", type=str, required=True, help="Path to write the JSON fix file to."
    )

    parser.add_argument(
        "-d", "--dsid", type=str, required=True, help="Dataset ID to create the fix template for."
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
                    "forcing_description": "derive: daops.fix_utils.decadal_utils.get_decadal_model_attr_from_dict: forcing_description",
                    "physics_description": "derive: daops.fix_utils.decadal_utils.get_decadal_model_attr_from_dict: physics_description",
                    "initialization_description": "derive: daops.fix_utils.decadal_utils.get_decadal_model_attr_from_dict: initialization_description",
                    "startdate": "derive: daops.fix_utils.decadal_utils.get_sub_experiment_id",
                    "sub_experiment_id": "derive: daops.fix_utils.decadal_utils.get_sub_experiment_id",
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
                "value": "derive: daops.fix_utils.decadal_utils.get_reftime",
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
                "value": "derive: daops.fix_utils.decadal_utils.get_lead_times",
                "dim": ["time"],
                "dtype": "float64",
                "attrs": {
                    "long_name": "Time elapsed since the start of the forecast",
                    "standard_name": "forecast_period",
                    "units": "days"
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
            "operands": {"var_ids": "derive: daops.fix_utils.decadal_utils.get_decadal_bnds_list"},
            "source": {
                "name": "ceda",
                "version": "",
                "comments": "",
                "url": "https://github.com/cp4cds/c3s34g_master/tree/master/Decadal",
            },
        },
    ],
}


def get_decadal_template():
    "Takes a copy of the global template, and returns it."
    tmpl = copy.deepcopy(decadal_template)
    return tmpl 


def main():
    args = arg_parse()

    fpath = args.fpath
    ds_id = args.dsid

    data_path = dsid_to_datapath(ds_id)

    # put into template
    dt = get_decadal_template()

    dt["dataset_id"] = ds_id

    # save the template as a json file
    with open(fpath, "w") as fp:
        json.dump(dt, fp, indent=4)


if __name__ == "__main__":
    main()

