import argparse
import collections
import json

import SETTINGS
from lib import options, utils



def _get_arg_parser():
    parser = argparse.ArgumentParser()
    project_options = options.known_projects

    parser.add_argument(
        "project",
        nargs=1,
        type=str,
        choices=project_options,
        help=f'Project ID, must be one of: {project_options}'
    )

    parser.add_argument(
        "-d",
        "--dataset-ids",
        nargs=1,
        type=str,
        default=None,
        required=True,
        help='List of comma-separated dataset identifiers'
    )

    return parser


def parse_args():
    parser = _get_arg_parser()
    args = parser.parse_args()

    project = args.project[0]
    ds_ids = args.dataset_ids[0].split(',')

    return project, ds_ids


def _lookup(item, *keys):

    keys = list(keys)
    
    while keys:
        k0 = keys[0]
        item = item[k0]
        keys.remove(k0)

    return item
        

def analyse_characteristic(records, *keys):
    
    results = {}
    count = 0

    for ds_id, rec in records.items():
        
        result = _lookup(rec, *keys)
        results.setdefault(result, [])
        results[result].append(ds_id)
        count += 1

    print(f'\n[INFO] Testing: {keys} - found {len(results)} varieties')
    for key in sorted(results):

        ds_ids = results[key]
        print(f'\t{keys} == {key}:   {len(ds_ids)}')
        count_ratio = float(len(ds_ids)) / count

        if count_ratio < SETTINGS.CONCERN_THRESHOLD:
            print(f'\t[WARN] SUGGEST FIX OF {keys} ON:\n\t\t' + '\n\t\t'.join(ds_ids))
    

def analyse_datasets(project, ds_ids):
    "Compares a set of dataset identifiers"
    records = load_records(ds_ids)

    analyse_characteristic(records, 'data', 'rank')
    analyse_characteristic(records, 'coordinates', 'time', 'calendar')


def load_records(ds_ids):

    records = collections.OrderedDict()

    for ds_id in ds_ids:

        grouped_ds_id = utils.get_grouped_ds_id(ds_id)

        json_path = SETTINGS.JSON_OUTPUT_PATH.format(**vars())

        with open(json_path) as reader:
            records[ds_id] = json.load(reader)
        

    return records
    

def main():
    
    project, ds_ids = parse_args()
    analyse_datasets(project, ds_ids)


if __name__ == '__main__':

    main()

