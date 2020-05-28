# dachar (pron. "day-car")

[![Pypi](https://img.shields.io/pypi/v/dachar.svg)](https://pypi.python.org/pypi/dachar)

[![Travis](https://img.shields.io/travis/ellesmith88/dachar.svg)](https://travis-ci.com/github/roocs/dachar)

[![Documentation](https://readthedocs.org/projects/dachar/badge/?version=latest)](https://dachar.readthedocs.io/en/latest/?badge=latest)

The "dachar" package (pronounced "day-car", like René Descartes, a founder of modern science and philosophy)
is a python library used to capture and analyse the _character_ of scientific data sets. We typically focus on data sets held in the 
Earth System Grid Federation (ESGF) catalogues. 

ESGF data sets are usually defined by the following characteristics:

 * an identifier (string) that consists of an ordered set of facet values with a version identifier
 * a single 2D or 3D geophysical variable over multiple time steps
 * represented in one or more NetCDF files

Examples ESGF data sets are:
 * **CMIP5**: `cmip5.output1.MPI-M.MPI-ESM-LR.decadal1995.mon.land.Lmon.r5i1p1.v20120529`
 * **CORDEX**: `cordex.output.AFR-44.DMI.ECMWF-ERAINT.evaluation.r1i1p1.HIRHAM5.v2.day.uas.v20140804`

* Free software: BSD
* Documentation: https://dachar.readthedocs.io.


## Features

There are three main stages to the characterisation process:

 1. **Scan**: Scan all data sets and write a character file (JSON).
 2. **Analysis**: Define _populations_ of data sets (that might be processed together)
 and analyse each _population_ to identify irregularities when comparing
 with other members of the population. Write the results of the analysis (JSON).
 3. **Define Fixes**: Suggest fixes required to individual data sets to overcome the 
 irregularities. Write the required fixes to a new set of files (JSON). 

# Credits

This package was created with `Cookiecutter` and the `cedadev/cookiecutter-pypackage` project template.

 * Cookiecutter: https://github.com/audreyr/cookiecutter
 * cookiecutter-pypackage: https://github.com/cedadev/cookiecutter-pypackage
