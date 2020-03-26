# -*- coding: utf-8 -*-

"""Console script for dachar."""

__author__ = """Elle Smith"""
__contact__ = "eleanor.smith@stfc.ac.uk"
__copyright__ = "Copyright 2018 United Kingdom Research and Innovation"
__license__ = "BSD"
import argparse
import sys


def main():
    """Console script for dachar."""
    parser = argparse.ArgumentParser()
    parser.add_argument('_', nargs='*')
    args = parser.parse_args()

    print("Arguments: " + str(args._))
    print("Replace this message by putting your code into "
          "dachar.cli.main")
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
