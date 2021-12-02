from dachar.fixes._base_fix import _BaseDatasetFix
from dachar.utils.common import UNDEFINED

__all__ = ["AddDataVarFix"]


class AddDataVarFix(_BaseDatasetFix):
    fix_id = "AddDataVarFix"
    title = "Add a variable"
    description = """
Takes the variable to add along with its attributes

For example:
  - inputs:
    - {'var_id': 'realization',
       'value': '1',
       'dtype': 'int32',
       'attrs': {'long_name': 'realization',
                 'comment': 'example'}
      }

    """

    category = "var_fixes"
    required_operands = ["dtype", "var_id", "value", "attrs"]
    ref_implementation = "daops.data_utils.var_utils.add_data_var"
    process_type = "post_processor"
