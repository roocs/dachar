from dachar.analyse.checks._base_check import _BaseCheck
from dachar.fixes.fix_api import get_fix
from pprint import pprint

__all__ = ['RankCheck']


class RankCheck(_BaseCheck):
    characteristics = ['data.coord_names']#, 'data.shape']
    associated_fix = 'SqueezeDimensionsFix'

    def deduce_fix(self, ds_id, atypical_content, typical_content):
        # x = atypical_content['data.coord_names']

        fix_cls = get_fix(self.associated_fix)
        operands = {'dims': 1}

        fix = fix_cls(ds_id, **operands)
        d = fix.to_dict()
        pprint(d)
        return d

    # dict of ds_id and fix?
