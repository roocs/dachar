import importlib
import pprint as pp

from dachar.fixes._base_fix import _BaseDatasetFix
from dachar.fixes.fix_api import get_fix
from dachar.fixes.fix_api import get_fix_categories
from dachar.fixes.fix_api import get_fix_dict


def test_get_fix_categories():
    expected_fix_categories = ["array_fixes", "attr_fixes", "coord_fixes", "var_fixes"]
    assert get_fix_categories() == expected_fix_categories

    expected_fix_dict = {
        "coord_fixes": ["SqueezeDimensionsFix", "AddScalarCoordFix", "AddCoordFix"],
        "array_fixes": [],
        "attr_fixes": [
            "GlobalAttrFix",
            "CheckAddGlobalAttrFix",
            "VarAttrFix",
            "RemoveCoordAttrFix",
        ],
        "var_fixes": ["AddDataVarFix"],
    }
    assert get_fix_dict() == expected_fix_dict


def _get_props(obj):
    return [attr for attr in dir(obj) if not attr.startswith("_")]


def test_fix_definitions():
    # Find all fixes and then test they have sensible definitions
    required_properties = [
        "fix_id",
        "title",
        "description",
        "required_operands",
        # "template",
        # "ncml_template",
    ]
    errors = ""

    for category, fixes in get_fix_dict().items():
        mod = importlib.import_module(f"dachar.fixes.{category}")

        for fix in fixes:
            cls = getattr(mod, fix)
            cls_props = _get_props(cls)

            if not set(required_properties).issubset(set(cls_props)):
                errors += f"Error in Fix properties for class {cls.__name__}:\n"

                missing_props = set(required_properties).difference(set(cls_props))
                if missing_props:
                    errors += f"\tRequired properties not defined: {missing_props}\n"

            cls_category = getattr(cls, "category", None)
            if cls_category != category:
                errors += f"\tDeduced category does not match category in class: {cls_category} != {category}\n for fix {fix}"

    if errors:
        raise Exception(errors)


class _TestFix(_BaseDatasetFix):

    fix_id = "TestFix"
    title = "Test Fix Test"
    description = "Test description"

    category = "test_fixes"
    required_operands = ["thing", "other"]
    ref_implementation = "daops.test.test"
    process_type = "post_processor"

    ncml_template = '<JustStuff info="{thing}">{other}</JustStuff>'

    # template = {
    #   'fix_id': 'fix_id',
    #   'title': 'title',
    #   'description': 'description',
    #   'category': 'category',
    #   'reference_implementation': 'ref_implementation',
    #   'ds_id': 'ds_id',
    #   'operands': 'operands'
    # }


source = {
    "name": "dachar",
    "version": "test",
    "comment": "No specific source provided - link to all fixes in dachar",
    "url": "https://github.com/roocs/dachar/tree/master/dachar/fixes",
}


def test_eg_fix():
    fix = _TestFix("ds1", thing=23, other="hello", source=source)
    assert fix.description == _TestFix.description

    expected_dict = {
        "dataset_id": {"ds_id": "ds1"},
        "fix": {
            "fix_id": _TestFix.fix_id,
            "title": _TestFix.title,
            "description": _TestFix.description,
            "category": _TestFix.category,
            "reference_implementation": _TestFix.ref_implementation,
            "process_type": _TestFix.process_type,
            "operands": {"thing": 23, "other": "hello"},
            "source": {
                "name": "dachar",
                "version": "test",
                "comment": "No specific source provided - link to all fixes in dachar",
                "url": "https://github.com/roocs/dachar/tree/master/dachar/fixes",
            },
        },
    }

    assert fix.to_ncml() == '<JustStuff info="{thing}">{other}</JustStuff>'.format(
        **fix.operands
    )
    assert fix.to_dict() == expected_dict

    expected_repr = f"""<Fix: {_TestFix.fix_id} (category: {_TestFix.category})>

{_TestFix.description}

Operands: {{'thing': 23, 'other': 'hello'}}
"""
    assert repr(fix) == expected_repr
