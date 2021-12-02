# -*- coding: utf-8 -*-
__author__ = """Elle Smith"""
__contact__ = "eleanor.smith@stfc.ac.uk"
__copyright__ = "Copyright 2018 United Kingdom Research and Innovation"
__license__ = "BSD"

import argparse
import sys
from dachar import CONFIG
from dachar.index.create_index import (
    create_index_and_alias,
    clone_index_and_update_alias,
    populate_store,
    add_document_to_index,
    delete_index,
)
from dachar.utils.get_stores import get_store_by_name


def _get_arg_parser_create(parser):
    """
    Parses arguments given at the command line

    :return: Namespace object built from attributes parsed from command line.
    """

    parser.add_argument(
        "-i",
        "--index",
        type=str,
        required=True,
        help=f"index to create, can be one of fix, character, analysis, fix-proposal",
    )

    parser.add_argument(
        "-u",
        "--update-alias",
        action="store_true",
        help=f"If provided the alias will be updated with the newly created index.",
    )

    return parser


def parse_args_create(args):
    index = args.index

    if index == "fix":
        index_name = CONFIG["elasticsearch"]["fix_store"]

    elif index == "fix-proposal":
        index_name = CONFIG["elasticsearch"]["fix_proposal_store"]

    elif index == "analysis":
        index_name = CONFIG["elasticsearch"]["analysis_store"]

    elif index == "character":
        index_name = CONFIG["elasticsearch"]["character_store"]

    elif index == "test":
        index_name = CONFIG["elasticsearch"]["test"]

    else:
        raise Exception(
            f"index {index} should be one of fix, fix-proposal, character or analysis"
        )

    update_alias = args.update_alias

    return index_name, update_alias


def create_main(args):
    index_name, update_alias = parse_args_create(args)
    create_index_and_alias(index_name, update_alias=update_alias)


def _get_arg_parser_delete(parser):
    """
    Parses arguments given at the command line

    :return: Namespace object built from attributes parsed from command line.
    """

    parser.add_argument(
        "-i", "--index", type=str, required=True, help=f"index to delete",
    )

    return parser


def parse_args_delete(args):
    index = args.index

    return index


def delete_main(args):
    index_name = parse_args_delete(args)
    delete_index(index_name)


def _get_arg_parser_clone(parser):

    parser.add_argument(
        "-i",
        "--index",
        type=str,
        required=True,
        help=f"index to create, can be one of fix, character, analysis, fix-proposal",
    )

    parser.add_argument(
        "-c", "--clone", type=str, required=True, help=f"Name of the index to clone",
    )

    parser.add_argument(
        "-u",
        "--update-alias",
        action="store_true",
        help=f"If provided the alias will be updated with the newly created index.",
    )

    return parser


def parse_args_clone(args):
    index = args.index

    update_alias = args.update_alias

    if index == "fix":
        index_name = CONFIG["elasticsearch"]["fix_store"]

    elif index == "fix-proposal":
        index_name = CONFIG["elasticsearch"]["fix_proposal_store"]

    elif index == "analysis":
        index_name = CONFIG["elasticsearch"]["analysis_store"]

    elif index == "character":
        index_name = CONFIG["elasticsearch"]["character_store"]

    elif index == "test":
        index_name = CONFIG["elasticsearch"]["test"]

    else:
        raise Exception(
            f"index {index} should be one of fix, fix-proposal, character or analysis"
        )

    clone = args.clone

    return index_name, clone, update_alias


def clone_main(args):
    index_name, clone, update_alias = parse_args_clone(args)
    clone_index_and_update_alias(index_name, clone, update_alias=update_alias)


def _get_arg_parser_populate(parser):

    parser.add_argument(
        "-s",
        "--store",
        type=str,
        required=True,
        help="Name of local store to use to populate elasticsearch index, can be one of fix, character, analysis, fix-proposal",
    )

    parser.add_argument(
        "-i", "--index", type=str, required=True, help=f"Name of index to populate",
    )

    return parser


def parse_args_populate(args):
    store = args.store
    index = args.index
    return store, index


def populate_main(args):
    store, index = parse_args_populate(args)
    store_object = get_store_by_name(store)

    if store == "analysis":
        id_type = "sample_id"

    else:
        id_type = "dataset_id"

    populate_store(store_object, index, id_type)


def _get_arg_parser_add_doc(parser):

    parser.add_argument(
        "-f",
        "--fpath",
        type=str,
        required=True,
        help="File path of document to add to index.",
    )

    parser.add_argument(
        "-d",
        "--drs",
        type=str,
        required=True,
        help="The dataset id or sample id for which the document is being added.",
    )

    parser.add_argument(
        "-i",
        "--index",
        type=str,
        required=True,
        help="Name of index to add document to",
    )

    return parser


def parse_args_add_doc(args):
    fpath = args.fpath
    drs = args.drs
    index = args.index

    return fpath, drs, index


def add_doc_main(args):
    fpath, drs, index = parse_args_add_doc(args)

    store = ("-").join(index.split("-")[:-3])
    if store == "analysis":
        id_type = "sample_id"

    else:
        id_type = "dataset_id"

    add_document_to_index(fpath, drs, index, id_type)


def main():
    """Console script for dachar."""
    main_parser = argparse.ArgumentParser()
    subparsers = main_parser.add_subparsers()

    create_parser = subparsers.add_parser("create")
    _get_arg_parser_create(create_parser)
    create_parser.set_defaults(func=create_main)

    delete_parser = subparsers.add_parser("delete")
    _get_arg_parser_delete(delete_parser)
    delete_parser.set_defaults(func=delete_main)

    clone_parser = subparsers.add_parser("clone")
    _get_arg_parser_clone(clone_parser)
    clone_parser.set_defaults(func=clone_main)

    populate_parser = subparsers.add_parser("populate")
    _get_arg_parser_populate(populate_parser)
    populate_parser.set_defaults(func=populate_main)

    add_doc_parser = subparsers.add_parser("add-document")
    _get_arg_parser_add_doc(add_doc_parser)
    add_doc_parser.set_defaults(func=add_doc_main)

    args = main_parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    sys.exit(main())
