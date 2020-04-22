import importlib

from dachar.fixes.fix_api import get_fix_categories, get_fix_dict

def test_get_fix_categories():
    expected_fix_categories = ['coord_fixes']
    assert(get_fix_categories() == expected_fix_categories)

    expected_fix_dict = {'coord_fixes': ['SqueezeDimensionsFix']}
    assert(get_fix_dict() == expected_fix_dict)


def _get_props(obj):
    return [attr for attr in dir(obj) if not attr.startswith('_')]


def test_fix_definitions():
    # Find all fixes and then test they have sensible definitions
    required_properties = ['fix_id', 'title', 'description', 'required_kwargs', 'json_template', 'ncml_template']
    errors = ''

    for category, fixes in get_fix_dict().items():
        mod = importlib.import_module(f'dachar.fixes.{category}')

        for fix in fixes:
            cls = getattr(mod, fix)
            cls_props = _get_props(cls)

            if not set(required_properties).issubset(set(cls_props)):
                errors += f'Error in Fix properties for class {cls.__name__}:\n'

                missing_props = set(required_properties).difference(set(cls_props))
                if missing_props:
                    errors += f'\tRequired properties not defined: {missing_props}\n'

            cls_category = getattr(cls, 'category', None)
            if cls_category != category:
                errors += f'\tDeduced category does not match category in class: {cls_category} != {category}\n'

    if errors:
        raise Exception(errors)

