
dachar (pron. "day-car")
========================


.. image:: https://img.shields.io/pypi/v/dachar.svg
   :target: https://pypi.python.org/pypi/dachar
   :alt: Pypi



.. image:: https://img.shields.io/travis/roocs/dachar.svg
   :target: https://travis-ci.org/github/roocs/dachar
   :alt: Travis



.. image:: https://readthedocs.org/projects/dachar/badge/?version=latest
   :target: https://dachar.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation


The "dachar" package (pronounced "day-car", like René Descartes, a founder of modern science and philosophy)
is a python library used to capture and analyse the *character* of scientific data sets. We typically focus on data sets held in the
Earth System Grid Federation (ESGF) catalogues.

ESGF data sets are usually defined by the following characteristics:


* an identifier (string) that consists of an ordered set of facet values with a version identifier
* a single 2D or 3D geophysical variable over multiple time steps
* represented in one or more NetCDF files

Examples ESGF data sets are:


* **CMIP5**\ : ``cmip5.output1.MPI-M.MPI-ESM-LR.decadal1995.mon.land.Lmon.r5i1p1.v20120529``
* **CORDEX**\ : ``cordex.output.AFR-44.DMI.ECMWF-ERAINT.evaluation.r1i1p1.HIRHAM5.v2.day.uas.v20140804``


* Free software: BSD
* Documentation: https://dachar.readthedocs.io.

Features
--------

There are three main stages to the characterisation process:


#. **Scan**\ : Scan all data sets and write a character file (JSON).
#. **Analysis**\ : Define *populations* of data sets (that might be processed together)
   and analyse each *population* to identify irregularities when comparing
   with other members of the population. Write the results of the analysis (JSON).
#. **Define Fixes**\ : Suggest fixes required to individual data sets to overcome the
   irregularities. Write the required fixes to a new set of files (JSON).

Credits
=======

This package was created with ``Cookiecutter`` and the ``cedadev/cookiecutter-pypackage`` project template.


* Cookiecutter: https://github.com/audreyr/cookiecutter
* cookiecutter-pypackage: https://github.com/cedadev/cookiecutter-pypackage
