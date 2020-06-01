#!/usr/bin/env python

from dachar.utils import switch_ds
import argparse
import glob
import subprocess
import re


def arg_parse():
    parser = argparse.ArgumentParser()

    parser.add_argument('-p', '--path', type=str, required=True)

    return parser.parse_args()


def convert_to_ds_id_and_scan(args):
    project = 'c3s-cmip5'
    ensemble_path = args.path
    vars = glob.glob(f'{ensemble_path}/*')

    for var_path in vars:
        versions = glob.glob(f'{var_path}/*')

        ds_ids = []
        for version_path in versions:
            ds_id = switch_ds.switch_ds(project, version_path)

            if re.search(r'^v', ds_id.split('.')[-1]):
                ds_ids.append(ds_id)

        ds_id_list = str(ds_ids).strip("[]").replace(' ','').replace("'", "")

        # print(ds_id_list)
        cmd = f'dachar scan -l ceda -d {ds_id_list} -m full {project}'
        subprocess.call(cmd, shell=True)


def main():
    args = arg_parse()
    convert_to_ds_id_and_scan(args)


if __name__ == '__main__':
    main()

