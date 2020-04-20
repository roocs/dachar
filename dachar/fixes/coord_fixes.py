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
    required_kwargs = ['dims']
    ref_implementation = 'daops.post_processors.squeeze_dims'

    ncml_template = """
      <variable name="temperature">
        <logicalReduce dimNames="latitude longitude" />
      </variable>
      """

    json_template = """{{
      "fix_id": "{self.fix_id}",
      "title": "{self.title}",
      "description": "{self.description}",
      "category": "{self.category}",
      "reference_implementation": "{self.ref_implementation}",
      "ds_id": "{self.ds_id}",
      "kwargs": "{self.kwargs}"
      }}"""
