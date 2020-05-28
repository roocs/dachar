# -*- coding: utf-8 -*-
"""Console script for dachar."""

__author__ = """Elle Smith"""
__contact__ = "eleanor.smith@stfc.ac.uk"
__copyright__ = "Copyright 2018 United Kingdom Research and Innovation"
__license__ = "BSD"
import argparse
import sys

from dachar.utils import options
from dachar import scan, analyse, fixes


def _to_list(item):
    if not item:
        return item
    return item[0].split(",")


def _to_dict(item):
    if not item:
        return item
    return dict([_.split("=") for _ in item[0].split(",")])


def _get_arg_parser_scan(parser):
    """
    Parses arguments given at the command line

    :return: Namespace object built from attributes parsed from command line.
    """
    # parser = argparse.ArgumentParser()
    project_options = options.known_projects
    location_options = options.locations

    parser.add_argument(
        "project",
        nargs=1,
        type=str,
        choices=project_options,
        help=f"Project ID, must be one of: {project_options}",
    )

    parser.add_argument(
        "-d",
        "--dataset-ids",
        nargs=1,
        type=str,
        default=None,
        required=False,
        help="List of comma-separated dataset identifiers",
    )

    parser.add_argument(
        "-p",
        "--paths",
        nargs=1,
        type=str,
        default=None,
        required=False,
        help="List of comma-separated directories to search",
    )

    parser.add_argument(
        "-f",
        "--facets",
        nargs=1,
        type=str,
        default=None,
        required=False,
        help="Set of facets to use, formatted as: x=hello,y=2,z=bye",
    )

    parser.add_argument(
        "-e",
        "--exclude",
        nargs=1,
        type=str,
        default=None,
        required=False,
        help="Regular expressions for excluding paths from being scanned",
    )

    parser.add_argument(
        "-m",
        "--mode",
        nargs=1,
        type=str,
        default="quick",
        required=False,
        help="Scanning mode: can be either quick or full. A full scan returns "
        "max and min values while a quick scan excludes them. Defaults to quick.",
    )

    parser.add_argument(
        "-l",
        "--location",
        nargs=1,
        type=str,
        default="ceda",
        required=True,
        choices=location_options,
        help=f"Location of scan, must be one of: {location_options}",
    )

    return parser


def parse_args_scan(args):
    project = args.project[0]
    ds_ids = _to_list(args.dataset_ids)
    paths = _to_list(args.paths)
    facets = _to_dict(args.facets)
    exclude = _to_list(args.exclude)
    mode = args.mode[0]
    location = args.location[0]

    return project, ds_ids, paths, facets, exclude, mode, location


def scan_main(args):
    project, ds_ids, paths, facets, exclude, mode, location = parse_args_scan(args)
    scan.scan_datasets(project, mode, location, ds_ids, paths, facets, exclude)


def _get_arg_parser_analyse(parser):
    project_options = options.known_projects

    parser.add_argument(
        "project",
        nargs=1,
        type=str,
        choices=project_options,
        help=f"Project ID, must be one of: {project_options}",
    )

    parser.add_argument(
        "-d",
        "--dataset-ids",
        nargs=1,
        type=str,
        default=None,
        required=True,
        help="List of comma-separated dataset identifiers",
    )

    return parser


def parse_args_analyse(args):
    project = args.project[0]
    ds_ids = args.dataset_ids[0].split(",")

    return project, ds_ids


def analyse_main(args):
    project, ds_ids = parse_args_analyse(args)
    analyse.analyse_datasets(project, ds_ids)


def write_fixes_main(args):
    pass


def main():
    """Console script for dachar."""
    main_parser = argparse.ArgumentParser()
    subparsers = main_parser.add_subparsers()

    scan_parser = subparsers.add_parser("scan")
    _get_arg_parser_scan(scan_parser)
    scan_parser.set_defaults(func=scan_main)

    analyse_parser = subparsers.add_parser("analyse")
    _get_arg_parser_analyse(analyse_parser)
    analyse_parser.set_defaults(func=analyse_main)

    fix_parser = subparsers.add_parser("write-fixes")
    # _get_arg_parser_fixes(fix_parser)
    fix_parser.set_defaults(func=write_fixes_main)

    args = main_parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
