from dachar.fixes._base_fix import _BaseDatasetFix
from dachar.utils.common import UNDEFINED

__all__ = ["MaskDataFix"]


class MaskDataFix(_BaseDatasetFix):
    fix_id = "MaskDataFix"
    title = "Apply Mask to Data"
    description = """
Masks data equal to a given value.

For example:
  - inputs:
    - {'value': '1.0e33'}
"""
    category = "array_fixes"
    required_operands = ["value"]
    ref_implementation = "daops.data_utils.array_utils.mask_data"
    process_type = "post_processor"
