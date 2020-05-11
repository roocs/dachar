from dachar.analyse.checks._base_check import _BaseCheck
from dachar.fixes.fix_api import get_fix
from dachar.utils.common import get_extra_items_in_larger_sequence


class RankCheck(_BaseCheck):
    characteristics = ['data.coord_names', 'data.shape']
    associated_fix = 'SqueezeDimensionsFix'

    def deduce_fix(self, ds_id, atypical_content, typical_content):

        atypical = atypical_content['data.coord_names']
        typical = typical_content['data.coord_names']
        if len(atypical) > len(typical):
            extra_coords = get_extra_items_in_larger_sequence(typical, atypical)

        else:
            extra_coords = get_extra_items_in_larger_sequence(atypical, typical)

        if extra_coords:

            if len(extra_coords) > 0:

                fix_cls = get_fix(self.associated_fix)

                for coord in extra_coords:
                    index = extra_coords.index(coord)
                    if atypical_content['data.shape'][index] != 1:
                        extra_coords.remove(coord)

                operands = {'dims': extra_coords}

                fix = fix_cls(ds_id, **operands)
                d = fix.to_dict()
                return d

        # fix isn't suitable
        else:
            return None

