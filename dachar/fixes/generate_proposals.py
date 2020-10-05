import json
from pydoc import locate
from dachar.utils.get_stores import get_fix_prop_store


def generate_fix_proposals(files):
    for file in files:
        if isinstance(file, dict):
            proposal = file
        else:
            with open(file) as f:
                proposal = json.load(f)

        category, fix_id = proposal.get('category'), proposal.get('fix_id')
        fix_cls = locate(f"dachar.fixes.{fix_id}")

        ds_id, source, operands = proposal.get('dataset_id'), proposal.get('source'), proposal.get('operands')

        fix = fix_cls(ds_id, source=source, **operands)
        d = fix.to_dict()

        get_fix_prop_store().propose(
            d["dataset_id"]["ds_id"], d["fix"]
        )


def generate_proposal_from_template(template, ds_list):
    with open(template) as f:
        proposal_template = json.load(f)

    proposals = []
    with open(ds_list, "r") as f1:
        for line in f1:
            ds_id = line.strip()
            proposal_template = proposal_template.copy()
            proposal_template["dataset_id"] = ds_id
            proposals.append(proposal_template)
    
    generate_fix_proposals(proposals)
