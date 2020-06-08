# -*- coding: utf-8 -*-
import os
import shutil

from dachar.utils._stores_for_tests import _TestFixProposalStore
"""Console script for dachar."""

__author__ = """Elle Smith"""
__contact__ = "eleanor.smith@stfc.ac.uk"
__copyright__ = "Copyright 2018 United Kingdom Research and Innovation"
__license__ = "BSD"
import argparse
import sys

from dachar.utils import options
from dachar.scan.scan import scan_datasets
from dachar.analyse.sample_analyser import analyse
from dachar.fixes import process_fixes
from dachar.fixes.process_fixes import process_all_fixes
from unittest.mock import Mock


def _to_list(item):
    if not item: return item
    return item.split(',')


def _to_dict(item):
    if not item: return item
    return dict([_.split('=') for _ in item.split(',')])


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
        type=str,
        choices=project_options,
        help=f'Project ID, must be one of: {project_options}'
    )

    parser.add_argument(
        "-d",
        "--dataset-ids",
        type=str,
        default=None,
        required=False,
        help='List of comma-separated dataset identifiers'
    )

    parser.add_argument(
        "-p",
        "--paths",
        type=str,
        default=None,
        required=False,
        help='List of comma-separated directories to search'
    )

    parser.add_argument(
        "-fs",
        "--facets",
        type=str,
        default=None,
        required=False,
        help='Set of facets to use, formatted as: x=hello,y=2,z=bye'
    )

    parser.add_argument(
        "-e",
        "--exclude",
        type=str,
        default=None,
        required=False,
        help='Regular expressions for excluding paths from being scanned'
    )

    parser.add_argument(
        "-m",
        "--mode",
        type=str,
        default="quick",
        required=False,
        help='Scanning mode: can be either quick or full. A full scan returns '
             'max and min values while a quick scan excludes them. Defaults to quick.'
             'Setting mode=full-force will overwrite any scans already completed in '
             'quick mode.'
    )

    parser.add_argument(
        "-l",
        "--location",
        type=str,
        default="ceda",
        required=True,
        choices=location_options,
        help=f'Location of scan, must be one of: {location_options}'
    )

    return parser


def parse_args_scan(args):
    project = args.project
    ds_ids = _to_list(args.dataset_ids)
    paths = _to_list(args.paths)
    facets = _to_dict(args.facets)
    exclude = _to_list(args.exclude)
    mode = args.mode
    location = args.location

    return project, ds_ids, paths, facets, exclude, mode, location


def scan_main(args):
    project, ds_ids, paths, facets, exclude, mode, location = parse_args_scan(args)
    scan_datasets(project, mode, location, ds_ids, paths, facets, exclude)


def _get_arg_parser_analyse(parser):
    project_options = options.known_projects
    location_options = options.locations

    parser.add_argument(
        "project",
        type=str,
        choices=project_options,
        help=f'Project ID, must be one of: {project_options}'
    )

    parser.add_argument(
        "-s",
        "--sample-id",
        type=str,
        default=None,
        required=True,
        help='Sample id with * indicating the facets that change '
    )

    parser.add_argument(
        "-l",
        "--location",
        type=str,
        default="ceda",
        required=True,
        choices=location_options,
        help=f'Location of scan, must be one of: {location_options}'
    )

    parser.add_argument(
        "-f",
        "--force",
        type=str,
        default=False,
        help=f'If True then analysis records will be overwritten if they already exist.'
    )

    return parser


def parse_args_analyse(args):
    project = args.project
    sample_id = args.sample_id
    location = args.location
    force = args.force

    return project, sample_id, location, force


def analyse_main(args):
    project, sample_id, location, force = parse_args_analyse(args)
    analyse(project, sample_id, location, force)


def _get_arg_parser_process_fixes(parser):

    parser.add_argument(
        "-d",
        "--dataset-ids",
        type=str,
        default=None,
        required=False,
        help='List of comma-separated dataset identifiers'
    )

    parser.add_argument(
        "-a",
        "--action",
        type=str,
        default=None,
        required=True,
        help='Action to carry out on fixes: process for proposed fixes, withdraw to withdraw'
             'existing fixes'
    )

    return parser


def parse_args_process_fixes(args):
    ds_ids = _to_list(args.dataset_ids)
    action = args.action
    return ds_ids, action


def process_fixes_main(args):
    action, ds_ids = parse_args_process_fixes(args)
    process_all_fixes(action, ds_ids)


def main():
    """Console script for dachar."""
    main_parser = argparse.ArgumentParser()
    subparsers = main_parser.add_subparsers()

    scan_parser = subparsers.add_parser('scan')
    _get_arg_parser_scan(scan_parser)
    scan_parser.set_defaults(func=scan_main)

    analyse_parser = subparsers.add_parser('analyse')
    _get_arg_parser_analyse(analyse_parser)
    analyse_parser.set_defaults(func=analyse_main)

    fix_parser = subparsers.add_parser('process-fixes')
    _get_arg_parser_process_fixes(fix_parser)
    fix_parser.set_defaults(func=process_fixes_main)

    args = main_parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
