from dachar.fixes._base_fix import _BaseDatasetFix

__all__ = ["RemoveVarAttrFix"]


class RemoveVarAttrFix(_BaseDatasetFix):
    fix_id = "RemoveVarAttrFix"
    title = "Remove Attributes of any Variable"
    description = """
Removes the attributes of a given variables e.g. standard name
Takes a list of attributes to remove.
For example:
  - inputs:
    {"var_id": "lat",
    "attrs": ["standard_name", "units"]
    }
"""
    category = "attr_fixes"
    required_operands = ["var_id", "attrs"]
    ref_implementation = "daops.data_utils.attr_utils.remove_var_attrs"
    process_type = "post_processor"
