from dachar.fixes.coord_fixes import SqueezeDimensionsFix, AddScalarCoordFix


source = {
        "name": "dachar",
        "version": "test",
        "comment": "No specific source provided - link to all fixes in dachar",
        "url": "https://github.com/roocs/dachar/tree/master/dachar/fixes"}


def test_SqueezeDimensionsFix():
    fix = SqueezeDimensionsFix("cmip5.output1.INM.inmcm4.rcp45.mon.ocean.Omon.r1i1p1.latest.zostoga", dims="lev",
                               source=source)

    assert fix.fix_id == "SqueezeDimensionsFix"
    assert fix.title == "Squeeze singleton dimensions of the main variable"

    assert fix.category == "coord_fixes"
    assert fix.required_operands == ["dims"]
    assert fix.ref_implementation == "daops.data_utils.coord_utils.squeeze_dims"
    assert fix.process_type == "post_processor"

    assert fix.description == """
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


def test_AddScalarCoordFix():
    operands = {
        "dtype": "float64",
        "value": 2.0,
        "id": "height",
        "length": 1,
        "attrs": {
            "axis": "Z",
            "long_name": "height",
            "positive": "up",
            "standard_name": "height",
            "units": "m",
        },
    }

    fix = AddScalarCoordFix("cmip5.output1.ICHEC.EC-EARTH.historical.mon.atmos.Amon.r1i1p1.latest.tas", **operands,
                            source=source)

    assert fix.fix_id == "AddScalarCoordFix"
    assert fix.title == "Add a coordinate"

    assert fix.category == "coord_fixes"
    assert fix.required_operands == ["dtype", "id", "value", "length", "attrs"]
    assert fix.ref_implementation == "daops.data_utils.coord_utils.add_scalar_coord"
    assert fix.process_type == "post_processor"

    assert fix.description == """
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