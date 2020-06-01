# scan all c3s-cmip5 datasets using lotus
from dachar import config
from dachar.utils import switch_ds
import glob
import os
import subprocess

# glob.glob('/group_workspaces/jasmin2/cp4cds1/vol1/data/c3s-cmip5/output1/*/*/*/*/*/*/*/*')

# cordex: /group_workspaces/jasmin2/cp4cds1/vol1/data/c3s-cordex/output/EUR-11/

# cmip5: /group_workspaces/jasmin2/cp4cds1/vol1/data/c3s-cmip5/output1/


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

        ds_id = switch_ds.switch_ds('c3s-cmip5', ensemble_path)
        grouped_ds_id = switch_ds.get_grouped_ds_id(ds_id)
        output_base = config.BATCH_OUTPUT_PATH.format(grouped_ds_id=grouped_ds_id)

        dr = os.path.dirname(output_base)

        if not os.path.isdir(dr):
            os.makedirs(dr)


        # submit to lotus
        bsub_command = f"bsub -q {config.QUEUE} -W {config.WALLCLOCK} -o " \
                       f"{output_base}.out -e {output_base}.err {current_directory}" \
                       f"/scan_chunk.py -p {ensemble_path}"

        # bsub_command = f'{current_directory}/scan_chunk.py -p {ensemble_path}'
        subprocess.call(bsub_command, shell=True)

        print(f"running {bsub_command}")


def main():
    get_institute_model_combination()


if __name__ == '__main__':
    main()


