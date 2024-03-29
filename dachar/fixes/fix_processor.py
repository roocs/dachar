import pprint
from collections import namedtuple

from dachar.utils.get_stores import get_fix_prop_store
from dachar.utils.get_stores import get_fix_store


PROC_ACTIONS = namedtuple(
    "ACTIONS",
    ["PUBLISH", "PUBLISH_ALL", "REJECT", "REJECT_ALL"],
    defaults=["publish", "publish-all", "reject", "reject-all"],
)()
# in python 3.9 _fields_defaults is renamed _field_defaults
# ALLOWED_PROC_ACTIONS = sorted(PROC_ACTIONS._fields_defaults.values())


def get_proposed_fixes(ds_ids=None):
    if ds_ids is None:
        proposed_fixes = get_fix_prop_store().get_proposed_fixes()
    else:
        proposed_fixes = []

        for ds_id in ds_ids:
            proposed_fix_list = get_fix_prop_store().get_proposed_fix_by_id(ds_id)
            if proposed_fix_list is not None:
                for fix in proposed_fix_list:
                    proposed_fixes.append(fix)

    return proposed_fixes


def process_proposed_fixes(proposed_fixes):
    if len(proposed_fixes) > 0:
        for proposed_fix in proposed_fixes:

            ds_id = proposed_fix["dataset_id"]
            fix = proposed_fix["this_fix"]["fix"]

            # print fix so user can see what they are processing
            pprint.pprint(ds_id)
            pprint.pprint(fix)

            action = input(f"Enter action for proposed fix (publish or reject): ")

            if action not in ("publish", "reject"):
                action = input(f"Enter action for proposed fix (publish or reject): ")

            if action == PROC_ACTIONS.PUBLISH:
                get_fix_prop_store().publish(ds_id, fix)
                get_fix_store().publish_fix(ds_id, fix)

                print("[INFO] Fix has been published.")

            elif action == PROC_ACTIONS.REJECT:
                reason = input("Enter a reason for rejection: ")
                get_fix_prop_store().reject(ds_id, fix, reason)

                print("[INFO] Fix has been rejected.")

    else:
        raise Exception("No proposed fixes found.")


def get_fixes_to_withdraw(ds_ids):
    existing_fixes = []

    for ds_id in ds_ids:
        existing_fix = get_fix_store().get(ds_id)
        if existing_fix is not None:
            existing_fixes.append(existing_fix)

    return existing_fixes


def process_withdraw_fixes(existing_fixes):
    if len(existing_fixes) > 0:
        for existing_fix in existing_fixes:
            # fix = existing_fix["fixes"][0]
            ds_id = existing_fix["dataset_id"]

            # print fix so user can see what they are processing
            pprint.pprint(existing_fix)

            action = input("Withdraw fix(es)? [y/n]")

            if action == "y":

                fix_ids = input(
                    "Enter fix ids of the fixes to withdraw (comma separated & no spaces): "
                )
                fix_ids = fix_ids.split(",")

                withdrawn = []
                for fix_id in fix_ids:
                    print(fix_id)

                    for fix in existing_fix["fixes"]:
                        if fix["fix_id"] == fix_id:
                            reason = input("Enter a reason for withdrawal: ")

                            get_fix_prop_store().withdraw(ds_id, fix, reason)
                            get_fix_store().withdraw_fix(ds_id, fix_id)

                            withdrawn.append(fix_id)
                            print(f"[INFO] Fix {fix_id} has been withdrawn.")

                if set(withdrawn) != set(fix_ids):
                    missing_ids = list(set(fix_ids).difference(withdrawn))
                    print(f"[INFO] Fix id(s) {missing_ids} could not be found.")

            else:
                print("[INFO] No action taken.")
                pass

    else:
        raise Exception(
            "A fix could not be found."
        )  # include ds_id in this statement so user knows which one if many entered


def bulk_process_fixes(action):
    proposed_fixes = get_proposed_fixes(ds_ids=None)

    if action == PROC_ACTIONS.REJECT_ALL:
        reason = input("Enter a reason for rejection: ")

    if len(proposed_fixes) > 0:
        for proposed_fix in proposed_fixes:

            ds_id = proposed_fix["dataset_id"]
            fix = proposed_fix["this_fix"]["fix"]

            if action == PROC_ACTIONS.PUBLISH_ALL:
                get_fix_prop_store().publish(ds_id, fix)
                get_fix_store().publish_fix(ds_id, fix)

            elif action == PROC_ACTIONS.REJECT_ALL:
                get_fix_prop_store().reject(ds_id, fix, reason)

        print(f"[INFO] All fixes processed with action {action}")

    else:
        raise Exception("No proposed fixes found.")


def process_all_fixes(action, ds_ids=None):
    if action in ("publish-all", "reject-all"):
        bulk_process_fixes(action)

    elif action == "process":
        proposed_fixes = get_proposed_fixes(ds_ids)
        process_proposed_fixes(proposed_fixes)

    elif action == "withdraw":
        existing_fixes = get_fixes_to_withdraw(ds_ids)
        process_withdraw_fixes(existing_fixes)

    else:
        raise Exception(
            f"Expected action to be 'process', 'withdraw', 'publish-all', 'reject-all', recieved {action}"
        )
