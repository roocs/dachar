# -*- coding: utf-8 -*-
"""Top-level package for dachar."""

__author__ = """Elle Smith"""
__contact__ = "eleanor.smith@stfc.ac.uk"
__copyright__ = "Copyright 2018 United Kingdom Research and Innovation"
__license__ = "BSD"
__version__ = "0.1.0"

from roocs_utils.config import get_config

import dachar
CONFIG = get_config(dachar)

from .fixes import *
from .scan import *
from .utils import *
from .analyse import *