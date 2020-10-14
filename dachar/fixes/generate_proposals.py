import json
from pydoc import locate
from dachar.utils.get_stores import get_fix_prop_store


def flatten_proposal(d):
    keys = []
    for k, v in d.items():
        keys.append(k)
        if isinstance(v, list):
            for k1, v1 in v[0].items():
                keys.append(k1)
                if k1 == "source":
                    for k2, v2 in v1.items():
                        keys.append(k2)
    return keys


def validate_proposal(proposal):
    required = ["dataset_id", "fixes", "fix_id", "operands", "source", "name", "version", "comments", "url"]

    existing = flatten_proposal(proposal)

    missing = set(required).difference(set(existing))
    invalid = set(existing).difference(set(required))

    if missing:
        raise KeyError(
            f"Required fields not provided: {missing}"
        )

    if invalid:
        raise KeyError(
            f"Invalid fields provided: {invalid}"
        )


def generate_fix_proposals(files):
    for file in files:
        if isinstance(file, dict):
            proposal = file
        else:
            with open(file) as f:
                proposal = json.load(f)

        validate_proposal(proposal)
        ds_id = proposal.get('dataset_id')
        for prop in proposal.get('fixes'):
            fix_id = prop.get('fix_id')
            fix_cls = locate(f"dachar.fixes.{fix_id}")

            source, operands = prop.get('source'), prop.get('operands')

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


