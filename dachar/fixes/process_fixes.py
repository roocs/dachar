from dachar.utils.get_stores import get_fix_prop_store, get_fix_store


# def get_proposed_fixes(ds_ids):
#     proposed_fixes = []
#
#     for ds_id in ds_ids:
#         proposed_fix = get_fix_prop_store().get_proposed_fixes(ds_id)
#         if proposed_fix is not None:
#             proposed_fixes.append(proposed_fix)
#
#     return proposed_fixes


def get_proposed_fixes():
    proposed_fixes = get_fix_prop_store().get_proposed_fixes()
    return proposed_fixes


def process_proposed_fixes(proposed_fixes):
    for proposed_fix in proposed_fixes:
        fix = proposed_fix['fixes'][0]['fix']
        ds_id = proposed_fix['dataset_id']

        # print fix so user can see what they are processing
        print(type(proposed_fix))

        action = input("Enter action for proposed fix: ")

        if action == 'publish':
            get_fix_prop_store().publish(ds_id, fix)
            get_fix_store().publish_fix(ds_id, fix)

            print('[INFO] Fix has been published')

        if action == 'reject':
            reason = input("Enter a reason for rejection: ")
            get_fix_prop_store().reject(ds_id, fix, reason)

            print('[INFO] Fix has been rejected')

        else:
            pass


def process_all_fixes():
    proposed_fixes = get_proposed_fixes()
    process_proposed_fixes(proposed_fixes)
