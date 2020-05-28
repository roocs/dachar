import argparse
import collections
import json

from dachar import config
from dachar.utils import options
from dachar.utils import switch_ds


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

    print(f"\n[INFO] Testing: {keys} - found {len(results)} varieties")
    for key in sorted(results):

        ds_ids = results[key]
        print(f"\t{keys} == {key}:   {len(ds_ids)}")
        count_ratio = float(len(ds_ids)) / count

        if count_ratio < config.CONCERN_THRESHOLD:
            print(f"\t[WARN] SUGGEST FIX OF {keys} ON:\n\t\t" + "\n\t\t".join(ds_ids))


def analyse_datasets(project, ds_ids):
    "Compares a set of dataset identifiers"
    records = load_records(ds_ids)

    analyse_characteristic(records, "data", "rank")
    analyse_characteristic(records, "coordinates", "time", "calendar")


def load_records(ds_ids):

    records = collections.OrderedDict()

    for ds_id in ds_ids:

        grouped_ds_id = switch_ds.get_grouped_ds_id(ds_id)

        json_path = config.JSON_OUTPUT_PATH.format(**vars())

        with open(json_path) as reader:
            records[ds_id] = json.load(reader)

    return records
