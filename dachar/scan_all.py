# scan all c3s-cmip5 datasets using lotus

import glob

glob.glob('/group_workspaces/jasmin2/cp4cds1/vol1/data/c3s-cmip5/output1/*/*/*/*/*/*/*/*')


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



output_base = f"{lotus_output_path}/{ensemble}"

        # submit to lotus
        bsub_command = f"bsub -q {SETTINGS.QUEUE} -W {SETTINGS.WALLCLOCK} -o " \
                       f"{output_base}.out -e {output_base}.err {current_directory}" \
                       f"/run_chunk.py -s {stat} -m {model} -e {ensemble} -v {variables}"
        subprocess.call(bsub_command, shell=True)

        print(f"running {bsub_command}")
