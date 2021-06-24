from dachar.fixes._base_fix import _BaseDatasetFix

__all__ = ["ReplaceLatLonFillValuesFix"]


class ReplaceLatLonFillValuesFix(_BaseDatasetFix):
    fix_id = "ReplaceLatLonFillValuesFix"
    title = "Replaces a given value in latitude and longitude with a value of 1e+20 and sets this as the fill value in the encoding"
    description = """
Takes the value to replace in latitude and longitude
For example:
  - inputs:
    {'value': '1.0000000150474662e+30'}
"""
    category = "array_fixes"
    required_operands = ["value"]
    ref_implementation = "daops.data_utils.array_utils.replace_lat_and_lon_fill_values"
    process_type = "post_processor"
