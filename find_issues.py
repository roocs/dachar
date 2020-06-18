import glob
import xarray as xr
import os
import subprocess


def get_start(pattern):
    paths = glob.glob(f'{pattern}/*/*/*/')

    for p in paths:
        get_path(p)


def get_path(pattern):
    paths = glob.glob(f'{pattern}/*/*/vas/')

    for p in paths:
        get_datasets(p)
        
        
def get_datasets(pattern):
    paths = glob.glob(f'{pattern}/*/latest')

    for p in paths:
        output_base = f'./outputs{p}'

        dr = os.path.dirname(output_base)

        if not os.path.isdir(dr):
            os.makedirs(dr)

        current_directory = os.getcwd()
        # submit to lotus
        bsub_command = f'bsub -q short-serial -W 00:30 -o ' \
                       f'{output_base}.out -e {output_base}.err ' \
                       f'{current_directory}/lotus_script.py -p {p}'

        # bsub_command = f'{current_directory}/scan_vars.py -p {ensemble_path} -pr {project}'
        subprocess.call(bsub_command, shell=True)

        print(f"running {bsub_command}")


if __name__ == '__main__':
    get_start('/badc/cmip6/data/CMIP6/CMIP/')