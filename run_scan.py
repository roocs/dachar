from dachar.utils import switch_ds
import argparse
import glob
import subprocess


def arg_parse():
    parser = argparse.ArgumentParser()

    parser.add_argument('-p', '--path', type=str, required=True)

    return parser.parse_args()


def convert_to_ds_id_and_scan(args):
    project = 'c3s-cmip5'
    ensemble_path = args.path
    vars = glob.glob(f'{ensemble_path}/*')

    for var_path in vars:
        ds_id = switch_ds.switch_ds(project, var_path)
        print(ds_id)
        cmd = f'dachar scan -l ceda -d {ds_id} -m full {project}'
        # subprocess.call(cmd, shell=True)


def main():

    args = arg_parse()
    convert_to_ds_id_and_scan(args)


if __name__ == '__main__':
    main()

