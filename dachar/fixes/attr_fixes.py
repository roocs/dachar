from dachar.utils.common import UNDEFINED

from dachar.fixes._base_fix import _BaseDatasetFix

__all__ = ["MainVarAttrFix", "AttrFix"]


class MainVarAttrFix(_BaseDatasetFix):
    fix_id = "MainVarAttrFix"
    title = "Apply Fix to Attributes of Main Variable"
    description = """
"Applies metadata fix e.g. fixing standard name or adding missing standard name
 for the main variable of the dataset.

Takes a list of fixes with each fix as a dictionary containing the attribute
to be changed as the key and what the value should be as the value e.g.:

{"long_name": "Dissolved Oxygen Concentration"},
{"standard_name": "mole_concentration_of_dissolved_molecular_oxygen_in_sea_water"}

For example:
  - inputs:
    {"attrs": [
        {"long_name": "Dissolved Oxygen Concentration"},
        {"standard_name": "mole_concentration_of_dissolved_molecular_oxygen_in_sea_water"}
        ]
    },
"""
    category = "attr_fixes"
    required_operands = ["attrs"]
    ref_implementation = "daops.data_utils.attr_utils.fix_attr_main_var"
    process_type = "post_processor"


class AttrFix(_BaseDatasetFix):
    fix_id = "AttrFix"
    title = "Apply Fix to Attributes of any Variable"
    description = """
"Applies metadata fix e.g. fixing standard name or adding missing standard name
 for a given variable of the dataset.

Takes a list of fixes with each fix as a dictionary containing the attribute
to be changed as the key and what the value should be as the value e.g.:

{"long_name": "Dissolved Oxygen Concentration"},
{"standard_name": "mole_concentration_of_dissolved_molecular_oxygen_in_sea_water"}

For example:
  - inputs:
    {"var_id": "lev",
    "attrs": [
        {"long_name": "Dissolved Oxygen Concentration"},
        {"standard_name": "mole_concentration_of_dissolved_molecular_oxygen_in_sea_water"}
        ]
    },
"""
    category = "attr_fixes"
    required_operands = ["var_id", "attrs"]
    ref_implementation = "daops.data_utils.attr_utils.fix_attr"
    process_type = "post_processor"
