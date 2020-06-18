#!/usr/bin/env python

import argparse
import glob
import subprocess
import re
import xarray as xr


def arg_parse():
    parser = argparse.ArgumentParser()

    parser.add_argument('-p', '--pattern', type=str, required=True)
    return parser.parse_args()


def search_height(args):
    path = args.pattern
    ds = xr.open_mfdataset(f'{path}/*.nc', use_cftime=True, combine='by_coords')
    try:
        height = ds.height
        print('ok')
    except AttributeError:
        print(f'Height variable missing in dataset {path}')

        output_base = f'./outputs/missing{path}'

        dr = os.path.dirname(output_base)

        if not os.path.isdir(dr):
            os.makedirs(dr)


if __name__ == '__main__':
    args = arg_parse()
    search_height(args)