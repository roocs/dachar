from dachar.utils.common import UNDEFINED

from dachar.fixes._base_fix import _BaseDatasetFix

__all__ = ['SqueezeDimensionsFix']


class SqueezeDimensionsFix(_BaseDatasetFix):
    fix_id = 'SqueezeDimensionsFix'
    title = ' Squeeze singleton dimensions of the main variable'
    description = """
Takes a sequence of identifiers that specify the dimensions to be squeezed.

For each dimension:
  - check that the dimension is associated with the main variable
  - check that the dimension has a length of 1
  - remove the dimension from the variable metadata

For example:
  - inputs:
    - {'dims': ['level']}
  - input_variable:
    - dims = ['time', 'level']
    - shape = [1800, 1]
    - rank = 2
  - output_variable:
    - dims = ['time']
    - shape = [1800]
    - rank = 1
    """

    category = 'coord_fixes'
    required_operands = ['dims']
    ref_implementation = 'daops.post_processors.squeeze_dims'

    ncml_template = """
      <variable name="{self.variable***}">
        <logicalReduce dimNames="{' '.join(self.kwargs['dims'])}" />
      </variable>
      """
