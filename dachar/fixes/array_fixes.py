from dachar.utils.common import UNDEFINED

from dachar.fixes._base_fix import _BaseDatasetFix

__all__ = ["MaskMissingDataFix"]


class MaskMissingDataFix(_BaseDatasetFix):
    fix_id = "MetadataFix"
    title = "Apply Mask to Missing Data"
    description = """
Masks data equal to a given value. This value should be the value used to replace missing data.

For example:
  - inputs:
    - {'value': '1.0e33'}
"""
    category = "array_fixes"
    required_operands = ["value"]
    ref_implementation = "daops.data_utils.array_utils.mask_missing_data"
    process_type = "post_processor"
