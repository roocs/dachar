from dachar.utils.get_stores import get_fix_prop_store, get_fix_store
import pprint


def get_proposed_fixes(ds_ids=None):
    if ds_ids is None:
        proposed_fixes = get_fix_prop_store().get_proposed_fixes()
    else:
        proposed_fixes = []

        for ds_id in ds_ids:
            proposed_fix = get_fix_prop_store().get_proposed_fix_by_id(ds_id)
            if proposed_fix is not None:
                proposed_fixes.append(proposed_fix)

    return proposed_fixes


def process_proposed_fixes(proposed_fixes):
    if len(proposed_fixes) > 0:
        for proposed_fix in proposed_fixes:
            fix = proposed_fix["fixes"][0]["fix"]
            ds_id = proposed_fix["dataset_id"]

            # print fix so user can see what they are processing
            pprint.pprint(proposed_fix)

            action = input("Enter action for proposed fix: ")

            if action == "publish":
                get_fix_prop_store().publish(ds_id, fix)
                get_fix_store().publish_fix(ds_id, fix)

                print("[INFO] Fix has been published.")

            if action == "reject":
                reason = input("Enter a reason for rejection: ")
                get_fix_prop_store().reject(ds_id, fix, reason)

                print("[INFO] Fix has been rejected.")

            else:
                # print('[INFO] You have not selected an action for this fix.')
                pass

    else:
        print("[INFO] No proposed fixes found.")


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
            fix = existing_fix["fixes"][0]
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
                for id in fix_ids:
                    print(id)

                    for fix in existing_fix["fixes"]:
                        if fix["fix_id"] == id:
                            reason = input("Enter a reason for withdrawal: ")

                            get_fix_prop_store().withdraw(ds_id, fix, reason)
                            get_fix_store().withdraw_fix(ds_id, id)

                            withdrawn.append(id)
                            print(f"[INFO] Fix {id} has been withdrawn.")

                if set(withdrawn) != set(fix_ids):
                    missing_ids = list(set(fix_ids).difference(withdrawn))
                    print(f"[INFO] Fix id(s) {missing_ids} could not be found.")

            else:
                print("[INFO] No action taken.")
                pass

    else:
        print(
            "[INFO] A fix could not be found."
        )  # include ds_id in this statement so user knows which one if many entered


def process_all_fixes(action, ds_ids=None):
    if action == "process":

        proposed_fixes = get_proposed_fixes(ds_ids)
        process_proposed_fixes(proposed_fixes)

    if action == "withdraw":

        existing_fixes = get_fixes_to_withdraw(ds_ids)
        process_withdraw_fixes(existing_fixes)
