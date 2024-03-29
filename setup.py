#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""The setup script."""

__author__ = "Elle Smith"
__contact__ = "eleanor.smith@stfc.ac.uk"
__copyright__ = "Copyright 2018 United Kingdom Research and Innovation"
__version__ = "0.1.0"
__license__ = "BSD"

import os
from setuptools import setup, find_packages

# One strategy for storing the overall version is to put it in the top-level
# package's __init__ but Nb. test_json_store.py files are not needed to declare
# packages in Python 3

# Populate long description setting with content of README
#
# Use markdown format read me file as GitHub will render it automatically
# on package page
here = os.path.abspath(os.path.dirname(__file__))
_long_description = open(os.path.join(here, "README.rst")).read()

requirements = [line.strip() for line in open("requirements.txt")]

setup_requirements = [
    "pytest-runner",
]

test_requirements = ["pytest", "tox"]

docs_requirements = [
    "sphinx",
    "sphinx-rtd-theme",
    "nbsphinx",
    "pandoc",
    "ipython",
    "ipykernel",
    "jupyter_client",
    "matplotlib",
]


setup(
    author=__author__,
    author_email=__contact__,
    # See:
    # https://www.python.org/dev/peps/pep-0301/#distutils-trove-classification
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Environment :: Web Environment",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: BSD License",
        "Natural Language :: English",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Security",
        "Topic :: Internet",
        "Topic :: Scientific/Engineering",
        "Topic :: System :: Distributed Computing",
        "Topic :: System :: Systems Administration :: Authentication/Directory",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    description="dachar - data aware character.",
    license=__license__,
    # This qualifier can be used to selectively exclude Python versions -
    # in this case early Python 2 and 3 releases
    python_requires=">=3.6.0",
    entry_points={"console_scripts": ["dachar=dachar.cli:main",],},
    install_requires=[requirements,],
    long_description=_long_description,
    long_description_content_type="text/x-rst",
    include_package_data=True,
    keywords="dachar",
    name="dachar",
    packages=find_packages(include=["dachar", "dachar.*"]),
    package_data={"dachar": ["etc/roocs.ini"]},
    setup_requires=setup_requirements,
    test_suite="tests",
    tests_require=test_requirements,
    extras_require={"docs": docs_requirements},
    url="https://github.com/roocs/dachar",
    version=__version__,
    zip_safe=False,
)
