# scan all c3s-cmip5 datasets using lotus
from dachar import config
import glob
import os
import subprocess

# glob.glob('/group_workspaces/jasmin2/cp4cds1/vol1/data/c3s-cmip5/output1/*/*/*/*/*/*/*/*')


def get_institute_model_combination():
    models = glob.glob('/group_workspaces/jasmin2/cp4cds1/vol1/data/c3s-cmip5/output1/*/*/')

    # e.g. '/group_workspaces/jasmin2/cp4cds1/vol1/data/c3s-cmip5/output1/MOHC/HadGEM2-ES/'
    for model_path in models:
        get_frequency(model_path)


def get_frequency(model_path):
    frequencies = glob.glob(f'{model_path}/*/*')

    # e.g. '/group_workspaces/jasmin2/cp4cds1/vol1/data/c3s-cmip5/output1/MOHC/HadGEM2-ES/rcp45/mon'
    for freq_path in frequencies:
        get_ensemble(freq_path)


def get_ensemble(freq_path):
    ensembles = glob.glob(f'{freq_path}/*/*/*')

    for ensemble_path in ensembles:

        current_directory = os.getcwd()
        output_base = config.BATCH_OUTPUT_PATH # need to figure out how log paths works

        # submit to lotus
        # bsub_command = f"bsub -q {config.QUEUE} -W {config.WALLCLOCK} -o " \
        #                f"{output_base}.out -e {output_base}.err {current_directory}" \
        #                f"/run_scan.py -p {ensemble_path}"

        bsub_command = f'run_scan.py -p {ensemble_path}'
        subprocess.call(bsub_command, shell=True)

        print(f"running {bsub_command}")


def main():
    get_institute_model_combination()


if __name__ == '__main__':
    main()


