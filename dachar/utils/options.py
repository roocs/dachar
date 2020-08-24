import os
import sys

from roocs_utils import config 

project_base_dirs = config.project_base_dirs

if "ROOCS_CONFIG" in os.environ:
    config_path = os.environ["ROOCS_CONFIG"]
    sys.path.insert(1, config_path)
    import config_local as config
    project_base_dirs.update(config.project_base_dirs)


def get_project_base_dir(project):
    return project_base_dirs.get(project)


known_projects = project_base_dirs.keys()
locations = ["ceda", "dkrz", "other"]
facet_rules = {
    "cmip5": "activity product institute model experiment frequency realm mip_table ensemble_member version variable".split(),
    "cmip6": "mip_era activity_id institution_id source_id experiment_id member_id table_id variable_id grid_label version".split(),
    "cordex": "project product domain institute driving_model experiment ensemble rcm_name rcm_version time_frequency variable".split(),
    "c3s-cmip5": "activity product institute model experiment frequency realm mip_table ensemble_member variable version".split(),
    "c3s-cmip6": "mip_era activity_id institution_id source_id experiment_id member_id table_id variable_id grid_label version".split(),
    "c3s-cordex": "project product domain institute driving_model experiment ensemble rcm_name rcm_version time_frequency variable version".split(),
}
mappings = {"cmip6": {"variable": "variable_id"}}

# if coordinates are given different names but are equivalent
coord_mappings = {"ni": "i", "nj": "j", "i": "ni", "j": "nj"}

common_checks = ["coord_checks.RankCheck", "coord_checks.MissingCoordCheck"]
checks = {"cmip5": [], "cmip6": ["test"], "cordex": []}


def map_facet(facet, project):
    # Return mapped value or the same facet name
    proj_mappings = mappings.get(project, {})
    return proj_mappings.get(facet, facet)


def get_facet(facet_name, facets, project):
    return facets[map_facet(facet_name, project)]


def get_checks(project):
    # Return list of checks to carry out based on project
    project_checks = checks.get(project)
    return [*project_checks, *common_checks]


"""
dataset_id = cordex.%(product)s.%(domain)s.%(institute)s.%(driving_model)s.%(experiment)s.%(ensemble)s.%(rcm_name)s.%(rcm_version)s.%(time_frequency)s.%(variable)s

directory_format = %(root)s/%(project)s/%(product)s/%(domain)s/%(institute)s/%(driving_model)s/%(experiment)s/%(ensemble)s/%(rcm_model)s/%(rcm_version)s/%(time_frequency)s/%(variable)s/%(version)s
"""
