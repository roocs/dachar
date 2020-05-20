from dachar.utils.get_stores import get_fix_prop_store


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
        fix = proposed_fix['fixes']['fix']
        ds_id = proposed_fix['dataset_id']

        # print fix so user can see what they are processing
        print(fix)

        action = input("Enter action for proposed fix: ")

        if action == 'publish':
            get_fix_prop_store().publish(ds_id, fix)

        if action == 'reject':
            reason = input("Enter a reason for rejection: ")
            get_fix_prop_store().reject(ds_id, fix, reason)

        if action == 'ignore':
            pass


def process_all_fixes():
    proposed_fixes = get_proposed_fixes()
    process_proposed_fixes(proposed_fixes)
