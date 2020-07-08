import os
import glob
from pydoc import locate

import dachar.fixes.coord_fixes as coord_fixes


def get_fix_modules():
    module_dir = os.path.dirname(os.path.abspath(__file__))
    return glob.glob(f"{module_dir}/*_fixes.py")


def get_fix_categories():
    files = [os.path.basename(_) for _ in get_fix_modules()]
    return sorted([os.path.splitext(_)[0] for _ in files])


def get_fix_dict():
    "Returns a dictionary of {<category>: [<fixes>]}"
    d = {}

    for category in get_fix_categories():
        d[category] = eval(f"{category}.__all__")

    return d


def get_fix(fix_id):
    if fix_id:
        fix_cls = locate(f"dachar.fixes.coord_fixes.{fix_id}")
        return fix_cls


# example_fixes = {
#     'cmip5.output1.INM.inmcm4.rcp45.mon.ocean.Omon.r1i1p1.latest.zostoga': {
#         'pre_processor': {
#              'func': 'daops.pre_processors.do_nothing',
#              'args': None,
#              'kwargs': None,
#         },
#         'post_processor': {
#              'func': 'daops.post_processors.squeeze_dims',
#              'args': [1],
#              'kwargs': None,
#         },
#     }
# }

fix_template = {
    "dataset_id": "ds_id",
    "fix": {
        "fix_id": "fix_id",
        "title": "title",
        "description": "description",
        "category": "category",
        "reference_implementation": "ref_implementation",
        "operands": "operands",
    },
}
