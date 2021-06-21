
dachar (pron. "day-car")
========================


.. image:: https://img.shields.io/pypi/v/dachar.svg
   :target: https://pypi.python.org/pypi/dachar
   :alt: Pypi



.. image:: https://github.com/roocs/dachar/workflows/build/badge.svg
   :target: https://github.com/roocs/dachar/actions
   :alt: Build Status



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

See below for using the cli to scan, analyse, propose fixes and process fixes.
Character, analysis, fix and fix proposal records are stored on elasticsearch indices.
Creating, deleting and writing to indices is described below. The elastic api token must be set in ``etc/roocs.ini`` in order to do these actions.

Characterising
==============

Scanning
--------

.. code-block::

      $ dachar scan <project> -l <location>

e.g. ``dachar scan c3s-cmip6 -l ceda``. This will scan all c3s-cmip6 datasets.

There are 2 different scanning modes available - either quick or full. Use ``-m full`` or ``-m quick``. Quick scans can be overwritten with full scans using ``-m full-force``.

Use ``dachar scan -h`` to see the options available for scanning specific datasets.


Analysing
---------

To analyse populations of datasets. The sample id identifies the population to analyse.

.. code-block::

      $ dachar analyse -s <sample-id> <project> -l <location>

Using the flag `-f` will overwrite existing analysis records for the sample id.

Proposing Fixes
---------------

Analysis will automatically prpose fixes if any are found, however, if fixes are identified by another source they can be proposed.

There are different way of proposing fixes

1. By providing a JSON file of the fix. More than one JSON file can be provided.

.. code-block::

      $ dachar propose-fixes -f <json_file>,<json_file2>,<json_file3>

2. By providing a JSON template and a list of datasets that the fix should be proposed for.

.. code-block::

      $ dachar propose-fixes -t <json_template> -d <dataset_list>

See the directory ``tests/test_fixes/decadal_fixes`` for examples.

Note that if CMIP6 fixes are intended to be used for CDS datasets - the ds ids for the datasets must start with ``c3s-cmip6`` instead of ``CMIP6``.

Processing Fixes
----------------

To publish or reject proposed fixes use:

.. code-block::

      $ dachar process-fixes -a process

This can also be used as:

.. code-block::

      $ dachar process-fixes -a process -d <dataset-id>,<dataset-id>

to process specific fixes.

To withdraw existing fixes, use:

.. code-block::

      $ dachar process-fixes -a withdraw -d <dataset-id>,<dataset-id>


Adding to elasticsearch
=======================
When a new version of the index is being created:

1. A new index must be created with new date. This can be done by creating an empty index or cloning the old one.
   Creating an empty index will just make a new index with the date of creation and update the alias to point to it.
   Cloning creates a new index with the date of creation, fills it with all documents from the old index and updates the alias to point to it.

2. It can then be populated either with all documents in local store or one document at a time.


**Note** This isn't working yet
Cloning an index
----------------
To create an index with today's date and populate it with all documents from another index.

.. code-block::

      $ python dachar/index/cli.py clone -i <index-to-create> -c <index-to-clone>

e.g. ``python dachar/index/cli.py clone -i fix -c roocs-fix-2020-12-21``


Creating an empty index
-----------------------
To create an empty index with today's date.

.. code-block::

      $ python dachar/index/cli.py clone -i <index-to-create>

e.g. ``python dachar/index/cli.py clone -i fix``


Deleting an index
------------------
To delete an index.

.. code-block::

      $ python dachar/index/cli.py delete -i <index-to-delete>

e.g. ``python dachar/index/cli.py delete -i roocs-fix-2020-12-21``


Populating an index from a local json store
-------------------------------------------
Popluate an elasticsearch index with the contents of a local store.

.. code-block::

      $ python dachar/index/cli.py populate -s <store> -i <index-to-populate>

Store must be one of fix, fix-proposal, analysis or character.

e.g. ``python dachar/index/cli.py populate -s fix -i roocs-fix-2020-12-21``


Adding one document to an existing index
----------------------------------------
To add one document from any file path to a store

.. code-block::

      $ python dachar/index/cli.py add-document -f <file-path> -d <drs-id> -i <index>

drs-id is what the id is called in the index i.e. either dataset_id (for fix, character and fix proposal store) or sample_id (for the analysis store)

e.g. ``python dachar/index/cli.py add-document -f /path/to/doc.json -d c3s-cmip6.ScenarioMIP.INM.INM-CM5-0.ssp245.r1i1p1f1.Amon.rlds.gr1.v20190619 -i roocs-fix-2020-12-21``


Credits
=======

This package was created with ``Cookiecutter`` and the ``cedadev/cookiecutter-pypackage`` project template.


* Cookiecutter: https://github.com/audreyr/cookiecutter
* cookiecutter-pypackage: https://github.com/cedadev/cookiecutter-pypackage
