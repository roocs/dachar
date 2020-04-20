import os
import glob


import dachar.fixes.coord_fixes as coord_fixes


def get_fix_modules():
    module_dir = os.path.dirname(os.path.abspath(__file__))
    return glob.glob(f'{module_dir}/*_fixes.py')


def get_fix_categories():
    files = [os.path.basename(_) for _ in get_fix_modules()]
    return sorted([os.path.splitext(_)[0] for _ in files])


def get_fix_dict():
    "Returns a dictionary of {<category>: [<fixes>]}"
    d = {}

    for category in get_fix_categories():
        d[category] = eval(f'{category}.__all__')

    return d


get_fix_dict()

example_fixes = {
    'cmip5.output1.INM.inmcm4.rcp45.mon.ocean.Omon.r1i1p1.latest.zostoga': {
        'pre_processor': {
             'func': 'daops.pre_processors.do_nothing',
             'args': None,
             'kwargs': None,
        },
        'post_processor': {
             'func': 'daops.post_processors.squeeze_dims',
             'args': [1],
             'kwargs': None,
        },
    }
}


def OLD_write_fixes():

   ds_ids = ['cmip5.output1.INM.inmcm4.rcp45.mon.ocean.Omon.r1i1p1.latest.zostoga']

   for ds_id in ds_ids:

       grouped_ds_id = utils.get_grouped_ds_id(ds_id)
       json_path = SETTINGS.FIX_PATH.format(**vars())

       dr = os.path.dirname(json_path)
       if not os.path.isdir(dr):
           os.makedirs(dr)

       content = example_fixes

       with open(json_path, 'w') as writer:
           json.dump(content, writer, indent=4, sort_keys=True)

       print(f'[INFO] Wrote: {json_path}')

