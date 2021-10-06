#!/usr/bin/env python

print("""LATEST ISSUE: daops wants to know if the data is characterised!!!
- BUT MAYBE only if "pre_checked=True" in `rook` - so can probably ignore.
- BUT MIGHT WANT TO MAKE daops able to work with local fix store if easy.
""")

import time
import os

from dachar.utils.switch_ds import get_grouped_ds_id

basedir = "/badc/cmip6/data"

dsids = """
 /badc/cmip6/data/CMIP6/DCPP/CMCC/CMCC-CM2-SR5/dcppA-hindcast/s1960-r10i1p1f1/Amon/pr/gn/v20210719
 /badc/cmip6/data/CMIP6/DCPP/CMCC/CMCC-CM2-SR5/dcppA-hindcast/s1960-r10i1p1f1/Amon/psl/gn/v20210719
 /badc/cmip6/data/CMIP6/DCPP/CMCC/CMCC-CM2-SR5/dcppA-hindcast/s1960-r10i1p1f1/Amon/tas/gn/v20210719
 /badc/cmip6/data/CMIP6/DCPP/CMCC/CMCC-CM2-SR5/dcppA-hindcast/s1960-r1i1p1f1/Amon/pr/gn/v20210312
 /badc/cmip6/data/CMIP6/DCPP/CMCC/CMCC-CM2-SR5/dcppA-hindcast/s1960-r1i1p1f1/Amon/psl/gn/v20210312
 /badc/cmip6/data/CMIP6/DCPP/CMCC/CMCC-CM2-SR5/dcppA-hindcast/s1960-r1i1p1f1/Amon/tas/gn/v20210312
 /badc/cmip6/data/CMIP6/DCPP/CMCC/CMCC-CM2-SR5/dcppA-hindcast/s1960-r2i1p1f1/Amon/pr/gn/v20210312
 /badc/cmip6/data/CMIP6/DCPP/CMCC/CMCC-CM2-SR5/dcppA-hindcast/s1960-r2i1p1f1/Amon/psl/gn/v20210312
 /badc/cmip6/data/CMIP6/DCPP/CMCC/CMCC-CM2-SR5/dcppA-hindcast/s1960-r2i1p1f1/Amon/tas/gn/v20210312
""".strip().replace(basedir + "/", "").replace("/", ".").replace("CMIP6", "c3s-cmip6").split()


DS_LIST_FILE = "DSET_IDS.txt"
FIX_DIR = "./decadal_fixes"


def prep_dir(fpath):
    dr = os.path.dirname(fpath)
    if not os.path.isdir(dr):
        os.makedirs(dr)
    

def write_fix_file(dsid): 
    fix_file_path = os.path.join(FIX_DIR, get_grouped_ds_id(dsid) + ".json")
    prep_dir(fix_file_path)    
    cmd = f"ROOCS_CONFIG=MY_roocs.ini python generate_decadal_fix.py -f {fix_file_path} -d {dsid}"
    print(f"Running: {cmd}")
    os.system(cmd)
    return fix_file_path


def propose_fix(dsid):

    ds_file = "./dsid.txt"
    with open(ds_file, "w") as w: 
        w.write(dsid)

    print(f"Wrote dsid to: {ds_file}")
    fix_file_path = write_fix_file(dsid)

    cmd = f"ROOCS_CONFIG=MY_roocs.ini dachar propose-fixes --template {fix_file_path} --dataset-list {ds_file}"
    print(f"[INFO] Running: {cmd}")
    os.system(cmd)

    print("Sleeping...")
    time.sleep(1)


def main():

    prep_dir(FIX_DIR)
    print(f"[WARNING] QUESTION 1: Should I create indexes with: dachar/index/create_index.py ? Or just let them happen automatically?")
    
    for dsid in dsids:
        p = os.path.join(basedir, dsid.replace(".", "/")).replace("c3s-cmip6", "CMIP6")
        print(f"[INFO] Checking: {dsid}")

        if not os.path.isdir(p):
            raise Exception(f"[ERROR] {p} does not exist!")

        propose_fix(dsid)


if __name__ == "__main__":

    main()

