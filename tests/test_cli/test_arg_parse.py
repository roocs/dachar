# -*- coding: utf-8 -*-
import os
import shutil
import argparse
import sys

from dachar import CONFIG


def _to_list(item):
    if not item:
        return item
    return item.split(",")


def _to_dict(item):
    if not item:
        return item
    return dict([_.split("=") for _ in item.split(",")])


def example_arg_parse(args):
    parser = argparse.ArgumentParser()

    project_options = CONFIG['known_projects']
    location_options = CONFIG['dachar:settings']['locations']

    parser.add_argument(
        "project",
        type=str,
        choices=project_options,
        help=f"Project ID, must be one of: {project_options}",
    )

    parser.add_argument(
        "-d",
        "--dataset-ids",
        type=str,
        default=None,
        required=False,
        help="List of comma-separated dataset identifiers",
    )

    parser.add_argument(
        "-e",
        "--exclude",
        type=str,
        default=None,
        required=False,
        help="Regular expressions for excluding paths from being scanned",
    )

    parser.add_argument(
        "-m",
        "--mode",
        type=str,
        default="quick",
        required=False,
        help="Scanning mode: can be either quick or full. A full scan returns "
        "max and min values while a quick scan excludes them. Defaults to quick.",
    )

    parser.add_argument(
        "-l",
        "--location",
        type=str,
        default="ceda",
        required=True,
        choices=location_options,
        help=f"Location of scan, must be one of: {location_options}",
    )

    parser.add_argument(
        "-p",
        "--paths",
        type=str,
        default=None,
        required=False,
        help="List of comma-separated directories to search",
    )

    parser.add_argument(
        "-f",
        "--facets",
        type=str,
        default=None,
        required=False,
        help="Set of facets to use, formatted as: x=hello,y=2,z=bye",
    )

    return parser.parse_args(args)


def test_arg_parser_ds_ids():
    cmd = "dachar scan -l ceda -d cmip5.output1.MRI.MRI-CGCM3.rcp45.mon.ocean.Omon.r1i1p1.latest.zostoga -m full cmip5".split()
    parser = example_arg_parse(cmd[2:])
    assert parser.location == "ceda"
    assert parser.mode == "full"
    assert parser.project == "cmip5"
    assert (
        parser.dataset_ids
        == "cmip5.output1.MRI.MRI-CGCM3.rcp45.mon.ocean.Omon.r1i1p1.latest.zostoga"
    )
    assert (
        _to_list(parser.dataset_ids)[0]
        == "cmip5.output1.MRI.MRI-CGCM3.rcp45.mon.ocean.Omon.r1i1p1.latest.zostoga"
    )


def test_arg_parse_2_ds_ids():
    cmd = "dachar scan -l ceda -d cmip5.output1.MRI.MRI-CGCM3.rcp45.mon.ocean.Omon.r1i1p1.latest.zostoga,cmip5.output1.MOHC.HadGEM2-ES.rcp85.mon.atmos.Amon.r1i1p1.latest.tas -m full cmip5".split()
    parser = example_arg_parse(cmd[2:])
    assert (
        parser.dataset_ids
        == "cmip5.output1.MRI.MRI-CGCM3.rcp45.mon.ocean.Omon.r1i1p1.latest.zostoga,cmip5.output1.MOHC.HadGEM2-ES.rcp85.mon.atmos.Amon.r1i1p1.latest.tas"
    )
    assert _to_list(parser.dataset_ids) == [
        "cmip5.output1.MRI.MRI-CGCM3.rcp45.mon.ocean.Omon.r1i1p1.latest.zostoga",
        "cmip5.output1.MOHC.HadGEM2-ES.rcp85.mon.atmos.Amon.r1i1p1.latest.tas",
    ]


def test_arg_parser_paths():
    cmd = "dachar scan -l ceda -p /badc/cmip6/data/CMIP6/AerChemMIP/MOHC/UKESM1-0-LL/piClim-2xNOx/r1i1p1f2/day -m full cmip6".split()
    parser = example_arg_parse(cmd[2:])
    assert (
        parser.paths
        == "/badc/cmip6/data/CMIP6/AerChemMIP/MOHC/UKESM1-0-LL/piClim-2xNOx/r1i1p1f2/day"
    )


def test_arg_parser_facets():
    facets = "activity=cmip5,product=output1,experiment=rcp45,frequency=mon,realm=ocean,mip_table=Omon,ensemble_member=r1i1p1,version=latest,variable=zostoga"
    cmd = f"dachar scan -l ceda -f {facets} -m quick cmip5".split()
    parser = example_arg_parse(cmd[2:])
    assert (
        parser.facets
        == "activity=cmip5,product=output1,experiment=rcp45,frequency=mon,realm=ocean,mip_table=Omon,ensemble_member=r1i1p1,version=latest,variable=zostoga"
    )
    assert _to_dict(parser.facets) == {
        "activity": "cmip5",
        "ensemble_member": "r1i1p1",
        "experiment": "rcp45",
        "frequency": "mon",
        "realm": "ocean",
        "mip_table": "Omon",
        "product": "output1",
        "version": "latest",
        "variable": "zostoga",
    }
