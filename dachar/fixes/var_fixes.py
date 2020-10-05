from dachar.utils.common import UNDEFINED

from dachar.fixes._base_fix import _BaseDatasetFix

__all__ = ["MetadataFix"]


class MetadataFix(_BaseDatasetFix):
    fix_id = "MetadataFix"
    title = "Apply Metadata Fix"
    description = """
"Applies metadata fix e.g. fixing standard name

Takes a list of fixes with each fix as a string containing the attribute
to be changed and what it will be changed to separated by a comma e.g.:

["long_name,Dissolved Oxygen Concentration",
"standard_name,mole_concentration_of_dissolved_molecular_oxygen_in_sea_water"]

For example:
  - inputs:
    {"fixes": [
        "long_name,Dissolved Oxygen Concentration",
        "standard_name,mole_concentration_of_dissolved_molecular_oxygen_in_sea_water"
        ]
    },
"""
    category = "var_fixes"
    required_operands = ["fixes"]
    ref_implementation = "daops.data_utils.var_utils.fix_metadata"
    process_type = "post_processor"
