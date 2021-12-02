from dachar.fixes._base_fix import _BaseDatasetFix
from dachar.utils.common import UNDEFINED

__all__ = [
    "GlobalAttrFix",
    "CheckAddGlobalAttrFix",
    "VarAttrFix",
    "RemoveFillValuesFix",
    "RemoveCoordAttrFix",
]


class GlobalAttrFix(_BaseDatasetFix):
    fix_id = "GlobalAttrFix"
    title = "Apply Fix to Global Attributes"
    description = """
Edits or adds global attributes e.g. fixing forcing description or institution_id.

Takes a dictionary of fixes with each fix as a key and value pair with the attribute
to be changed as the key and what the value should be as the value.

For example:
  - inputs:
    {"attrs":
        {"forcing_description": "Free text describing the forcings",
        "physics_description": "Free text describing the physics method"}
    },
"""
    category = "attr_fixes"
    required_operands = ["attrs"]
    ref_implementation = "daops.data_utils.attr_utils.edit_global_attrs"
    process_type = "post_processor"


class CheckAddGlobalAttrFix(_BaseDatasetFix):
    fix_id = "CheckAddGlobalAttrFix"
    title = "Add Global Attributes if missing"
    description = """
"Checks for the existence of a global attribute and adds it, only if it is missing.

Takes a dictionary of fixes with each fix as a key and value pair with the attribute
as the key and what the value should be as the value.

For example:
  - inputs:
    {"attrs":
        {"forcing_description": "Free text describing the forcings",
        "physics_description": "Free text describing the physics method"}
    },
"""
    category = "attr_fixes"
    required_operands = ["attrs"]
    ref_implementation = "daops.data_utils.attr_utils.add_global_attrs_if_needed"
    process_type = "post_processor"


class VarAttrFix(_BaseDatasetFix):
    fix_id = "VarAttrFix"
    title = "Apply Fix to Attributes of any Variable"
    description = """
Edits or adds the attributes of a given variables e.g. fixing standard name or adding missing standard name

Takes a dictionary of fixes with each fix as a key and value pair with the attribute
to be changed as the key and what the value should be as the value.

For example:
  - inputs:
    {"var_id": "lev",
    "attrs":
        {"long_name": "Dissolved Oxygen Concentration",
        "standard_name": "mole_concentration_of_dissolved_molecular_oxygen_in_sea_water"}
    }
"""
    category = "attr_fixes"
    required_operands = ["var_id", "attrs"]
    ref_implementation = "daops.data_utils.attr_utils.edit_var_attrs"
    process_type = "post_processor"


class RemoveFillValuesFix(_BaseDatasetFix):
    fix_id = "RemoveFillValuesFix"
    title = "Remove the Fill Value from coordinate variables"
    description = """
"Remove the FillValue attributes from coordinate variables which are added during manipulation with xarray, as NaNs.
"""
    category = "attr_fixes"
    required_operands = []
    ref_implementation = "daops.data_utils.attr_utils.remove_fill_values"
    process_type = "post_processor"


class RemoveCoordAttrFix(_BaseDatasetFix):
    fix_id = "RemoveCoordAttrFix"
    title = "Remove the coordinate attribute added by xarray from specified variables"
    description = """
"Remove the coordinate attribute from variables which is added during manipulation with xarray.
Takes the variable ids to remove the attribute from as a list.

For example:
    {"var_ids": ["realization", "time_bnds"]
    }
"""
    category = "attr_fixes"
    required_operands = ["var_ids"]
    ref_implementation = "daops.data_utils.attr_utils.remove_coord_attr"
    process_type = "post_processor"
