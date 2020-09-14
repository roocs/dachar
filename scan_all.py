# scan all c3s-cmip5 datasets using lotus
from dachar import CONFIG, logging
from dachar.utils import switch_ds
import glob
import os
import subprocess
import argparse

LOGGER = logging.getLogger(__file__)


# glob.glob('/group_workspaces/jasmin2/cp4cds1/vol1/data/c3s-cmip5/output1/*/*/*/*/*/*/*/*')

c3s_cordex_path = (
    "/group_workspaces/jasmin2/cp4cds1/vol1/data/c3s-cordex/output/EUR-11/"
)

c3s_cmip5_path = "/group_workspaces/jasmin2/cp4cds1/vol1/data/c3s-cmip5/output1/"


# workflow for scanning all:
# scan with small resource - full
# scan with large resource - full
# scan in quick mode


def arg_parse():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-pr",
        "--project",
        type=str,
        required=True,
        help="Project to scan, must be one of: c3s-cordex, c3s-cmip5",
    )
    parser.add_argument(
        "-r",
        "--resource",
        type=str,
        choices=["large", "small"],
        required=False,
        help="Resource requirement. Must be one of: large, small",
    )
    parser.add_argument(
        "-m",
        "--mode",
        type=str,
        required=True,
        choices=["quick", "full", "full-force"],
        help="Mode to scan in, must be one of: quick, full, full-force",
    )

    return parser.parse_args()


def get_file_path(args):
    project = args.project
    resource = args.resource
    mode = args.mode

    if project == "c3s-cordex":
        path = c3s_cordex_path
    elif project == "c3s-cmip5":
        path = c3s_cmip5_path
    else:
        raise Exception("Unknown Project")

    get_institute_model_combination(path, project, resource, mode)


def get_institute_model_combination(path, project, resource, mode):

    models = glob.glob(f"{path}*/*/")

    # e.g. '/group_workspaces/jasmin2/cp4cds1/vol1/data/c3s-cmip5/output1/MOHC/HadGEM2-ES/'
    for model_path in models:
        get_frequency(model_path, project, resource, mode)


def get_frequency(model_path, project, resource, mode):
    frequencies = glob.glob(f"{model_path}/*/*")

    # e.g. '/group_workspaces/jasmin2/cp4cds1/vol1/data/c3s-cmip5/output1/MOHC/HadGEM2-ES/rcp45/mon'
    for freq_path in frequencies:
        get_ensemble(freq_path, project, resource, mode)


def get_ensemble(freq_path, project, resource, mode):
    ensembles = glob.glob(f"{freq_path}/*/*/*")

    for ensemble_path in ensembles:

        current_directory = os.getcwd()

        ds_id = switch_ds.switch_ds(project, ensemble_path)
        grouped_ds_id = switch_ds.get_grouped_ds_id(ds_id)
        output_base = CONFIG['dachar:output_paths']['batch_output_path'].format(grouped_ds_id=grouped_ds_id)

        dr = os.path.dirname(output_base)

        if not os.path.isdir(dr):
            os.makedirs(dr)

        if resource == "large":
            wallclock = CONFIG['dachar:processing']['wallclock_large']
            memory_large = CONFIG['dachar:processing']['memory_large']
            memory_limit = (
                f'-R"rusage[mem={memory_large}]" -M {memory_large}'
            )
            memory_limit_slurm = f"--mem={memory_large}"

        else:
            wallclock = CONFIG['dachar:processing']['wallclock_small']
            memory_small = CONFIG['dachar:processing']['memory_small']
            memory_limit = (
                f'-R"rusage[mem={memory_small}]" -M {memory_small}'
            )
            memory_limit_slurm = f"--mem={memory_small}"

        # submit to lotus (LSF)
        queue = CONFIG['dachar:processing']['queue']
        bsub_command = (
            f"bsub -q {queue} -W {wallclock} -o "
            f"{output_base}.out -e {output_base}.err {memory_limit} "
            f"{current_directory}/scan_vars.py -p {ensemble_path} -pr {project} -m {mode}"
        )

        # to use with slurm:
        # sbatch_cmd = f'sbatch -p {queue} -t {wallclock} -o ' \
        #              f'{output_base}.out -e {output_base}.err {memory_limit_slurm} ' \
        #              f'{current_directory}/scan_vars.py -p {ensemble_path} -pr {project} -m {mode}'

        # bsub_command = f'{current_directory}/scan_vars.py -p {ensemble_path} -pr {project}'
        subprocess.call(bsub_command, shell=True)

        LOGGER.info(f"running {bsub_command}")


def main():
    args = arg_parse()
    get_file_path(args)


if __name__ == "__main__":
    main()
