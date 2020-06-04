# scan all c3s-cmip5 datasets using lotus
from dachar import config
from dachar.utils import switch_ds
import glob
import os
import subprocess

# glob.glob('/group_workspaces/jasmin2/cp4cds1/vol1/data/c3s-cmip5/output1/*/*/*/*/*/*/*/*')

c3s_cordex_path = '/group_workspaces/jasmin2/cp4cds1/vol1/data/c3s-cordex/output/EUR-11/'

c3s_cmip5_path = '/group_workspaces/jasmin2/cp4cds1/vol1/data/c3s-cmip5/output1/'


def get_project_to_run_over():
    project = input("Enter project to scan over: ")

    if project == 'c3s-cordex':
        path = c3s_cordex_path
    elif project == 'c3s-cmip5':
        path = c3s_cmip5_path
    else:
        raise Exception('Project must be one of c3s-cordex, c3s-cmip5')

    get_institute_model_combination(path, project)


def get_institute_model_combination(path, project):
    models = glob.glob(f'{path}*/*/')

    # e.g. '/group_workspaces/jasmin2/cp4cds1/vol1/data/c3s-cmip5/output1/MOHC/HadGEM2-ES/'
    for model_path in models:
        get_frequency(model_path, project)


def get_frequency(model_path, project):
    frequencies = glob.glob(f'{model_path}/*/*')

    # e.g. '/group_workspaces/jasmin2/cp4cds1/vol1/data/c3s-cmip5/output1/MOHC/HadGEM2-ES/rcp45/mon'
    for freq_path in frequencies:
        get_ensemble(freq_path, project)


def get_ensemble(freq_path, project):
    ensembles = glob.glob(f'{freq_path}/*/*/*')

    for ensemble_path in ensembles:

        current_directory = os.getcwd()

        ds_id = switch_ds.switch_ds(project, ensemble_path)
        grouped_ds_id = switch_ds.get_grouped_ds_id(ds_id)
        output_base = config.BATCH_OUTPUT_PATH.format(grouped_ds_id=grouped_ds_id)

        dr = os.path.dirname(output_base)

        if not os.path.isdir(dr):
            os.makedirs(dr)


        # submit to lotus
        bsub_command = f"bsub -q {config.QUEUE} -W {config.WALLCLOCK} -o " \
                       f"{output_base}.out -e {output_base}.err {current_directory}" \
                       f"/scan_chunk.py -p {ensemble_path} -pr {project}"

        # bsub_command = f'{current_directory}/scan_chunk.py -p {ensemble_path} -pr {project}'
        subprocess.call(bsub_command, shell=True)

        print(f"running {bsub_command}")


def main():
    get_project_to_run_over()


if __name__ == '__main__':
    main()


