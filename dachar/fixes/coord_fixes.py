from dachar.utils.common import UNDEFINED

from dachar.fixes._base_fix import _BaseDatasetFix

__all__ = ["SqueezeDimensionsFix", "AddScalarCoordFix"]


class SqueezeDimensionsFix(_BaseDatasetFix):
    fix_id = "SqueezeDimensionsFix"
    title = "Squeeze singleton dimensions of the main variable"
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

    category = "coord_fixes"
    required_operands = ["dims"]
    ref_implementation = "daops.data_utils.coord_utils.squeeze_dims"
    process_type = "post_processor"

    ncml_template = """
      <variable name="{self.variable***}">
        <logicalReduce dimNames="{' '.join(self.kwargs['dims'])}" />
      </variable>
      """


class AddScalarCoordFix(_BaseDatasetFix):
    fix_id = "AddScalarCoordFix"
    title = "Add a coordinate"
    description = """
Takes the coordinate to add along with its attributes

For example:
  - inputs:
    - {'id': 'height',
       'value': '2.0',
       'dtype': 'float64',
       'attrs': {'units': 'm'
                'standard_name': 'height'}}

Fix example: ds = ds.assign_coords(height=2.0) will add a scalar height coordinate with a value of 2.0
Attributes will be set by attrs: e.g. ds.attrs['units'] = 'm'
    """

    category = "coord_fixes"
    required_operands = ["dtype", "id", "value", "length", "attrs"]
    ref_implementation = "daops.data_utils.coord_utils.add_scalar_coord"
    process_type = "post_processor"
