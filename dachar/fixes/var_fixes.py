from dachar.fixes._base_fix import _BaseDatasetFix
from dachar.utils.common import UNDEFINED

__all__ = ["Reverse2DVarFix"]


class Reverse2DVarFix(_BaseDatasetFix):
    fix_id = "Reverse2DVarFix"
    title = "Reverse data of 2D Variables"
    description = """
"Reverses the order of the data of the given 2d variables

Takes as an input the names of the variables to be reversed
as a list:

For example:
  - inputs:
    {
    "var_ids": ["a_bnds", "b_bnds"]
    },
"""
    category = "var_fixes"
    required_operands = ["var_ids"]
    ref_implementation = "daops.data_utils.var_utils.reverse_2d_vars"
    process_type = "post_processor"
